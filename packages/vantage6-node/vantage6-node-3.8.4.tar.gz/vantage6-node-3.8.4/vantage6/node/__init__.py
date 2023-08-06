"""
A node in its simplest would retrieve a task from the central server by
an API call, run this task and finally return the results to the central
server again.

The node application runs four threads:

*Main thread*
    Checks the task queue and run the next task if there is one available.
*Listening thread*
    Listens for incoming websocket messages. Among other functionality, it adds
    new tasks to the task queue.
*Speaking thread*
    Waits for tasks to finish. When they do, return the results to the central
    server.
*Proxy server thread*
    Algorithm containers are isolated from the internet for security reasons.
    The local proxy server provides an interface to the central server for
    *master* containers to create subtasks and retrieve their results.

The node connects to the server using a websocket connection. This connection
is mainly used for sharing status updates. This avoids the need for polling to
see if there are new tasks available.
"""
import sys
import os
import random
import time
import datetime
import logging
import queue
import json
import shutil
import requests.exceptions

from pathlib import Path
from threading import Thread
from typing import Dict, List, Union, Type
from socketio import Client as SocketIO
from gevent.pywsgi import WSGIServer
from enum import Enum

from vantage6.common.docker.addons import (
    ContainerKillListener, check_docker_running, running_in_docker
)
from vantage6.common.globals import VPN_CONFIG_FILE, PING_INTERVAL_SECONDS
from vantage6.common.exceptions import AuthenticationException
from vantage6.common.docker.network_manager import NetworkManager
from vantage6.common.task_status import TaskStatus
from vantage6.cli.context import NodeContext
from vantage6.node.context import DockerNodeContext
from vantage6.node.globals import (
    NODE_PROXY_SERVER_HOSTNAME, SLEEP_BTWN_NODE_LOGIN_TRIES,
    TIME_LIMIT_RETRY_CONNECT_NODE, TIME_LIMIT_INITIAL_CONNECTION_WEBSOCKET
)
from vantage6.node.server_io import NodeClient
from vantage6.node import proxy_server
from vantage6.node.util import logger_name, get_parent_id
from vantage6.node.docker.docker_manager import DockerManager
from vantage6.node.docker.vpn_manager import VPNManager
from vantage6.node.socket import NodeTaskNamespace
from vantage6.node.docker.ssh_tunnel import SSHTunnel


class VPNConnectMode(Enum):
    FIRST_TRY = 1
    REFRESH_KEYPAIR = 2
    REFRESH_COMPLETE = 3


# ------------------------------------------------------------------------------
class Node(object):
    """
    Authenticates to the central server, setup encryption, a
    websocket connection, retrieving task that were posted while
    offline, preparing dataset for usage and finally setup a
    local proxy server..

    Parameters
    ----------
    ctx: Union[NodeContext, DockerNodeContext]
        Application context object.

    """
    def __init__(self, ctx: Union[NodeContext, DockerNodeContext]):

        self.log = logging.getLogger(logger_name(__name__))
        self.ctx = ctx

        # Initialize the node. If it crashes, shut down the parts that started
        # already
        try:
            self.initialize()
        except Exception:
            self.cleanup()
            raise

    def initialize(self) -> None:
        """Initialization of the node"""
        # check if docker is running, otherwise exit with error
        check_docker_running()

        self.config = self.ctx.config
        self.queue = queue.Queue()
        self._using_encryption = None

        # initialize Node connection to the server
        self.server_io = NodeClient(
            host=self.config.get('server_url'),
            port=self.config.get('port'),
            path=self.config.get('api_path')
        )

        self.log.info(f"Connecting server: {self.server_io.base_path}")

        # Authenticate with the server, obtaining a JSON Web Token.
        # Note that self.authenticate() blocks until it succeeds.
        self.log.debug("Authenticating")
        self.authenticate()

        # Setup encryption
        self.setup_encryption()

        # Thread for proxy server for algorithm containers, so they can
        # communicate with the central server.
        self.log.info("Setting up proxy server")
        t = Thread(target=self.__proxy_server_worker, daemon=True)
        t.start()

        # Create a long-lasting websocket connection.
        self.log.debug("Creating websocket connection with the server")
        self.connect_to_socket()

        # setup docker isolated network manager
        internal_ = running_in_docker()
        if not internal_:
            self.log.warn(
                "Algorithms have internet connection! "
                "This happens because you use 'vnode-local'!"
            )
        isolated_network_mgr = NetworkManager(self.ctx.docker_network_name)
        isolated_network_mgr.create_network(is_internal=internal_)

        # Setup tasks dir
        self._set_task_dir(self.ctx)

        # Setup VPN connection
        self.vpn_manager = self.setup_vpn_connection(
            isolated_network_mgr, self.ctx)

        # Create SSH tunnel according to the node configuration
        self.ssh_tunnels = self.setup_ssh_tunnels(isolated_network_mgr)

        # setup the docker manager
        self.log.debug("Setting up the docker manager")
        self.__docker = DockerManager(
            ctx=self.ctx,
            isolated_network_mgr=isolated_network_mgr,
            vpn_manager=self.vpn_manager,
            tasks_dir=self.__tasks_dir,
            client=self.server_io,
        )

        # Connect the node to the isolated algorithm network *only* if we're
        # running in a docker container.
        if self.ctx.running_in_docker:
            isolated_network_mgr.connect(
                container_name=self.ctx.docker_container_name,
                aliases=[NODE_PROXY_SERVER_HOSTNAME]
            )

        # Connect any docker services specified in the configuration file to
        # the node container
        self.link_docker_services()

        # Thread for sending results to the server when they come available.
        self.log.debug("Start thread for sending messages (results)")
        t = Thread(target=self.__speaking_worker, daemon=True)
        t.start()

        # listen forever for incoming messages, tasks are stored in
        # the queue.
        self.log.debug("Starting thread for incoming messages (tasks)")
        t = Thread(target=self.__listening_worker, daemon=True)
        t.start()

        self.log.info('Init complete')

    def __proxy_server_worker(self) -> None:
        """
        Proxy algorithm container communcation.

        A proxy for communication between algorithms and central
        server.
        """
        if self.ctx.running_in_docker:
            # NODE_PROXY_SERVER_HOSTNAME points to the name of the proxy
            # when running in the isolated docker network.
            default_proxy_host = NODE_PROXY_SERVER_HOSTNAME
        else:
            # If we're running non-dockerized, assume that the proxy is
            # accessible from within the docker algorithm container on
            # host.docker.internal.
            default_proxy_host = 'host.docker.internal'

        # If PROXY_SERVER_HOST was set in the environment, it overrides our
        # value.
        proxy_host = os.environ.get("PROXY_SERVER_HOST", default_proxy_host)
        os.environ["PROXY_SERVER_HOST"] = proxy_host

        proxy_port = int(os.environ.get("PROXY_SERVER_PORT", 8080))

        # 'app' is defined in vantage6.node.proxy_server
        # app.debug = True
        proxy_server.app.config["SERVER_IO"] = self.server_io
        proxy_server.server_url = self.server_io.base_path

        # this is where we try to find a port for the proxyserver
        for try_number in range(5):
            self.log.info(
                f"Starting proxyserver at '{proxy_host}:{proxy_port}'")
            http_server = WSGIServer(('0.0.0.0', proxy_port), proxy_server.app)

            try:
                http_server.serve_forever()

            except OSError as e:
                self.log.debug(f'Error during attempt {try_number}')
                self.log.debug(f'{type(e)}: {e}')

                if e.errno == 48:
                    proxy_port = random.randint(2048, 16384)
                    self.log.critical(
                        f"Retrying with a different port: {proxy_port}")
                    os.environ['PROXY_SERVER_PORT'] = str(proxy_port)

                else:
                    raise

            except Exception as e:
                self.log.error('Proxyserver could not be started or crashed!')
                self.log.error(e)

    def sync_task_queue_with_server(self) -> None:
        """ Get all unprocessed tasks from the server for this node."""
        assert self.server_io.cryptor, "Encrpytion has not been setup"

        # request open tasks from the server
        tasks = self.server_io.get_results(state="open", include_task=True)
        self.log.debug(tasks)
        for task in tasks:
            self.queue.put(task)

        self.log.info(f"received {self.queue._qsize()} tasks")

    def __start_task(self, taskresult: dict) -> None:
        """
        Start the docker image and notify the server that the task has been
        started.

        Parameters
        ----------
        taskresult : dict
            A dictionary with information required to run the algorithm
        """
        task = taskresult['task']
        self.log.info("Starting task {id} - {name}".format(**task))

        # notify that we are processing this task
        self.server_io.set_task_start_time(taskresult["id"])

        token = self.server_io.request_token_for_container(
            task["id"],
            task["image"]
        )
        token = token["container_token"]

        # create a temporary volume for each run_id
        vol_name = self.ctx.docker_temporary_volume_name(task["run_id"])
        self.__docker.create_volume(vol_name)

        # For some reason, if the key 'input' consists of JSON, it is
        # automatically marshalled? This causes trouble, so we'll serialize it
        # again.
        # FIXME: should probably find & fix the root cause?
        if type(taskresult['input']) == dict:
            taskresult['input'] = json.dumps(taskresult['input'])

        # Run the container. This adds the created container/task to the list
        # __docker.active_tasks
        task_status, vpn_ports = self.__docker.run(
            result_id=taskresult["id"],
            task_info=task,
            image=task["image"],
            docker_input=taskresult['input'],
            tmp_vol_name=vol_name,
            token=token,
            database=task.get('database', 'default')
        )

        # save task status to the server
        update = {'status': task_status}
        if task_status == TaskStatus.NOT_ALLOWED:
            # set finished_at to now, so that the task is not picked up again
            # (as the task is not started at all, unlike other crashes, it will
            # never finish and hence not be set to finished)
            update['finished_at'] = datetime.datetime.now().isoformat()
        self.server_io.patch_results(
            id=taskresult['id'], result=update
        )
        # send socket event to alert everyone of task status change
        self.socketIO.emit(
            'algorithm_status_change',
            data={
                'node_id': self.server_io.whoami.id_,
                'status': task_status,
                'result_id': taskresult['id'],
                'task_id': task['id'],
                'collaboration_id': self.server_io.collaboration_id,
                'organization_id': self.server_io.whoami.organization_id,
                'parent_id': get_parent_id(task),
            },
            namespace='/tasks',
        )

        if vpn_ports:
            # Save port of VPN client container at which it redirects traffic
            # to the algorithm container. First delete any existing port
            # assignments in case algorithm has crashed
            self.server_io.request(
                'port', params={'result_id': taskresult['id']}, method="DELETE"
            )
            for port in vpn_ports:
                port['result_id'] = taskresult['id']
                self.server_io.request('port', method='POST', json=port)

            # Save IP address of VPN container
            # FIXME BvB 2023-02-21: node IP is now updated when task is started
            # but this should be done when VPN connection is established
            node_id = self.server_io.whoami.id_
            node_ip = self.vpn_manager.get_vpn_ip()
            self.server_io.request(
                f"node/{node_id}", json={"ip": node_ip}, method="PATCH"
            )

    def __listening_worker(self) -> None:
        """
        Listen for incoming (websocket) messages from the server.

        Runs in a separate thread. Received events are handled by the
        appropriate action handler.
        """
        self.log.debug("Listening for incoming messages")

        # FIXME: while True in combination with a wait() call that never exits
        #   makes joining the tread (to terminate) difficult?
        while True:
            # incoming messages are handled by the action_handler instance
            # which is attached when the socket connection was made. wait()
            # is blocks forever (if no time is specified).
            try:
                self.socketIO.wait()
            except Exception as e:
                self.log.error('Listening thread had an exception')
                self.log.debug(e)

    def __speaking_worker(self) -> None:
        """
        Sending messages to central server.

        Routine that is in a seperate thread sending results
        to the server when they come available.
        """
        # TODO change to a single request, might need to reconsider
        #     the flow
        self.log.debug("Waiting for results to send to the server")

        while True:
            try:
                results = self.__docker.get_result()

                # notify socket channel of algorithm status change
                self.socketIO.emit(
                    'algorithm_status_change',
                    data={
                        'node_id': self.server_io.whoami.id_,
                        'status': results.status,
                        'result_id': results.result_id,
                        'task_id': results.task_id,
                        'collaboration_id': self.server_io.collaboration_id,
                        'organization_id':
                            self.server_io.whoami.organization_id,
                        'parent_id': results.parent_id,
                    },
                    namespace='/tasks',
                )

                self.log.info(
                    f"Sending result (id={results.result_id}) to the server!")

                # FIXME: why are we retrieving the result *again*? Shouldn't we
                # just store the task_id when retrieving the task the first
                # time?
                response = self.server_io.request(
                    f"result/{results.result_id}"
                )
                task_id = response.get("task").get("id")

                if not task_id:
                    self.log.error(
                        f"task_id of result (id={results.result_id}) "
                        f"could not be retrieved"
                    )
                    return

                response = self.server_io.request(f"task/{task_id}")

                init_org_id = response.get("initiator")
                if not init_org_id:
                    self.log.error(
                        f"Initiator organization from task (id={task_id})could"
                        " not be retrieved!"
                    )

                self.server_io.patch_results(
                    id=results.result_id,
                    result={
                        'result': results.data,
                        'log': results.logs,
                        'status': results.status,
                        'finished_at': datetime.datetime.now().isoformat(),
                    },
                    init_org_id=init_org_id,
                )
            except Exception:
                self.log.exception('Speaking thread had an exception')

    def __print_connection_error_logs(self):
        """ Print error message when node cannot find the server """
        self.log.warning(
            "Could not connect to the server. Retrying in 10 seconds")
        if self.server_io.host == 'http://localhost' and running_in_docker():
            self.log.warn(
                f"You are trying to reach the server at {self.server_io.host}."
                " As your node is running inside a Docker container, it cannot"
                " reach localhost on your host system. Probably, you have to "
                "change your serverl URL to http://host.docker.internal "
                "(Windows/MacOS) or http://172.17.0.1 (Linux)."
            )
        else:
            self.log.debug("Are you sure the server can be reached at "
                           f"{self.server_io.base_path}?")

    def authenticate(self) -> None:
        """
        Authenticate with the server using the api-key from the configuration
        file. If the server rejects for any reason -other than a wrong API key-
        serveral attempts are taken to retry.
        """

        api_key = self.config.get("api_key")

        success = False
        i = 0
        while i < TIME_LIMIT_RETRY_CONNECT_NODE / SLEEP_BTWN_NODE_LOGIN_TRIES:
            i = i + 1
            try:
                self.server_io.authenticate(api_key)

            except AuthenticationException as e:
                msg = "Authentication failed: API key is wrong!"
                self.log.warning(msg)
                self.log.debug(e)
                break
            except requests.exceptions.ConnectionError:
                self.__print_connection_error_logs()
                time.sleep(SLEEP_BTWN_NODE_LOGIN_TRIES)
            except Exception as e:
                msg = ('Authentication failed. Retrying in '
                       f'{SLEEP_BTWN_NODE_LOGIN_TRIES} seconds!')
                self.log.warning(msg)
                self.log.debug(e)
                time.sleep(SLEEP_BTWN_NODE_LOGIN_TRIES)

            else:
                # This is only executed if try-block executed without error.
                success = True
                break

        if success:
            self.log.info(f"Node name: {self.server_io.name}")
        else:
            self.log.critical('Unable to authenticate. Exiting')
            exit(1)

        # start thread to keep the connection alive by refreshing the token
        self.server_io.auto_refresh_token()

    def private_key_filename(self) -> Path:
        """Get the path to the private key."""

        # FIXME: Code duplication: vantage6/cli/node.py uses a lot of the same
        #   logic. Suggest moving this to ctx.get_private_key()
        filename = self.config['encryption']["private_key"]

        # filename may be set to an empty string
        if not filename:
            filename = 'private_key.pem'

        # If we're running dockerized, the location may have been overridden
        filename = os.environ.get('PRIVATE_KEY', filename)

        # If ctx.get_data_file() receives an absolute path, its returned as-is
        fullpath = Path(self.ctx.get_data_file(filename))

        return fullpath

    def setup_encryption(self) -> None:
        """ Setup encryption if the node is part of encrypted collaboration """
        encrypted_collaboration = self.server_io.is_encrypted_collaboration()
        encrypted_node = self.config['encryption']["enabled"]

        if encrypted_collaboration != encrypted_node:
            # You can't force it if it just ain't right, you know?
            raise Exception("Expectations on encryption don't match?!")

        if encrypted_collaboration:
            self.log.warn('Enabling encryption!')
            private_key_file = self.private_key_filename()
            self.server_io.setup_encryption(private_key_file)

        else:
            self.log.warn('Disabling encryption!')
            self.server_io.setup_encryption(None)

    def _set_task_dir(self, ctx) -> None:
        """
        Set the task dir

        Parameters
        ----------
        ctx: DockerNodeContext or NodeContext
            Context object containing settings
        """
        # If we're in a 'regular' context, we'll copy the dataset to our data
        # dir and mount it in any algorithm container that's run; bind mounts
        # on a folder will work just fine.
        #
        # If we're running in dockerized mode we *cannot* bind mount a folder,
        # because the folder is in the container and not in the host. We'll
        # have to use a docker volume instead. This means:
        #  1. we need to know the name of the volume so we can pass it along
        #  2. need to have this volume mounted so we can copy files to it.
        #
        #  Ad 1: We'll use a default name that can be overridden by an
        #        environment variable.
        #  Ad 2: We'll expect `ctx.data_dir` to point to the right place. This
        #        is OK, since ctx will be a DockerNodeContext.
        #
        #  This also means that the volume will have to be created & mounted
        #  *before* this node is started, so we won't do anything with it here.

        # We'll create a subfolder in the data_dir. We need this subfolder so
        # we can easily mount it in the algorithm containers; the root folder
        # may contain the private key, which which we don't want to share.
        # We'll only do this if we're running outside docker, otherwise we
        # would create '/data' on the data volume.
        if not ctx.running_in_docker:
            self.__tasks_dir = ctx.data_dir / 'data'
            os.makedirs(self.__tasks_dir, exist_ok=True)
            self.__vpn_dir = ctx.data_dir / 'vpn'
            os.makedirs(self.__vpn_dir, exist_ok=True)
        else:
            self.__tasks_dir = ctx.data_dir
            self.__vpn_dir = ctx.vpn_dir

    def setup_ssh_tunnels(self, isolated_network_mgr: Type[NetworkManager]) \
            -> List[SSHTunnel]:
        """
        Create a SSH tunnels when they are defined in the configuration file.
        For each tunnel a new container is created. The image used can be
        specified in the configuration file as `ssh-tunnel` in the `images`
        section, else the default image is used.

        Parameters
        ----------
        isolated_network_mgr: NetworkManager
            Manager for the isolated network
        """
        if 'ssh-tunnels' not in self.config:
            self.log.info("No SSH tunnels configured")
            return

        custom_tunnel_image = self.config.get('images', {}).get('ssh-tunnel') \
            if 'images' in self.config else None

        configs = self.config['ssh-tunnels']
        self.log.info(f"Setting up {len(configs)} SSH tunnels")

        tunnels: List[SSHTunnel] = []
        for config in configs:
            self.log.debug(f"SSH tunnel config: {config}")

            # copy (rename) the ssh key to the correct name, this is done so
            # that the file is in the volume (somehow we can not file mount
            # within a volume)
            if self.ctx.running_in_docker:
                ssh_key = f"/mnt/ssh/{config['hostname']}.pem.tmp"
                key_path = shutil.copy(ssh_key,
                                       f"/mnt/ssh/{config['hostname']}.pem")
                volume = self.ctx.docker_ssh_volume_name

            else:
                ssh_key = config['ssh']['identity']['key']

                volume = str(Path(ssh_key).parent)
                key_path = shutil.copy(ssh_key,
                                       f"{volume}/{config['hostname']}.pem")

            os.chmod(key_path, 0o600)

            try:
                new_tunnel = SSHTunnel(isolated_network_mgr, config,
                                       self.ctx.name, volume,
                                       custom_tunnel_image)
            except Exception as e:
                self.log.error("Error setting up SSH tunnel")
                self.log.debug(e, exc_info=True)
                continue

            tunnels.append(new_tunnel)

        return tunnels

    def setup_vpn_connection(self, isolated_network_mgr: NetworkManager,
                             ctx: Union[DockerNodeContext, NodeContext]
                             ) -> VPNManager:
        """
        Setup container which has a VPN connection

        Parameters
        ----------
        isolated_network_mgr: NetworkManager
            Manager for the isolated Docker network
        ctx: NodeContext
            Context object for the node

        Returns
        -------
        VPNManager
            Manages the VPN connection
        """
        ovpn_file = os.path.join(self.__vpn_dir, VPN_CONFIG_FILE)

        self.log.info("Setting up VPN client container")
        vpn_volume_name = self.ctx.docker_vpn_volume_name \
            if ctx.running_in_docker else self.__vpn_dir

        # FIXME: remove me in 4+. alpine image has been moved into the `images`
        # key. This is to support older configuration files.
        legacy_alpine = self.config.get('alpine')

        # user can specify custom images in the configuration file
        custom_alpine = self.config['images'].get('alpine') \
            if 'images' in self.config else None
        custom_vpn_client = self.config['images'].get('vpn_client') \
            if 'images' in self.config else None
        custom_network = self.config['images'].get('network_config') \
            if 'images' in self.config else None

        vpn_manager = VPNManager(
            isolated_network_mgr=isolated_network_mgr,
            node_name=self.ctx.name,
            vpn_volume_name=vpn_volume_name,
            vpn_subnet=self.config.get('vpn_subnet'),
            alpine_image=custom_alpine or legacy_alpine,
            vpn_client_image=custom_vpn_client,
            network_config_image=custom_network
        )

        if not self.config.get('vpn_subnet'):
            self.log.warn("VPN subnet is not defined! VPN disabled.")
        elif not os.path.isfile(ovpn_file):
            # if vpn config doesn't exist, get it and write to disk
            self._connect_vpn(vpn_manager, VPNConnectMode.REFRESH_COMPLETE,
                              ovpn_file)
        else:
            self._connect_vpn(vpn_manager, VPNConnectMode.FIRST_TRY, ovpn_file)

        return vpn_manager

    def _connect_vpn(self, vpn_manager: VPNManager,
                     connect_mode: VPNConnectMode, ovpn_file: str) -> None:
        """
        Connect to the VPN by starting up a VPN client container. If no VPN
        config file exists, we only try once after first obtaining a config
        file. If a VPN config file already exists, we first try to connect,
        then try to refresh the keypair, and finally try to renew the entire
        config file, until a connection is established.

        Parameters
        ----------
        vpn_manager: VPNManager
            Manages the VPN connection
        connect_mode: VPNConnectMode
            Specifies which parts of a config file to refresh before attempting
            to connect
        ovpn_file: str
            Path to the VPN configuration file
        """
        do_try = True
        if connect_mode == VPNConnectMode.FIRST_TRY:
            self.log.debug("Using existing config file to connect to VPN")
            next_mode = VPNConnectMode.REFRESH_KEYPAIR
        elif connect_mode == VPNConnectMode.REFRESH_KEYPAIR:
            self.log.debug("Refreshing VPN keypair...")
            do_try = self.server_io.refresh_vpn_keypair(ovpn_file=ovpn_file)
            next_mode = VPNConnectMode.REFRESH_COMPLETE
        elif connect_mode == VPNConnectMode.REFRESH_COMPLETE:
            self.log.debug("Requesting new VPN configuration file...")
            do_try = self._get_vpn_config_file(ovpn_file)
            next_mode = None  # if new config file doesn't work, give up

        if do_try:
            # try connecting to VPN
            try:
                vpn_manager.connect_vpn()
            except Exception as e:
                self.log.debug("Could not connect to VPN.")
                self.log.debug(f"Exception: {e}")
                # try again in another fashion
                if next_mode:
                    self._connect_vpn(vpn_manager, next_mode, ovpn_file)

    def _get_vpn_config_file(self, ovpn_file: str) -> bool:
        """
        Obtain VPN configuration file from the server

        Parameters
        ----------
        ovpn_file: str
            Path to the VPN configuration file

        Returns
        -------
        bool
            Whether or not configuration file was successfully obtained
        """
        # get the ovpn configuration from the server
        success, ovpn_config = self.server_io.get_vpn_config()
        if not success:
            self.log.warn("Obtaining VPN configuration file not successful!")
            self.log.warn("Disabling node-to-node communication via VPN")
            return False

        # write ovpn config to node docker volume
        with open(ovpn_file, 'w') as f:
            f.write(ovpn_config)
        return True

    def link_docker_services(self) -> None:
        docker_services = self.ctx.config.get("docker_services")
        if not docker_services:
            return
        self.log.info("Linking docker services specified in the configuration")
        for alias, container_name in docker_services.items():
            self.__docker.link_container_to_network(
                container_name=container_name, config_alias=alias
            )

    def connect_to_socket(self) -> None:
        """
        Create long-lasting websocket connection with the server. The
        connection is used to receive status updates, such as new tasks.
        """
        self.socketIO = SocketIO(request_timeout=60)

        self.socketIO.register_namespace(NodeTaskNamespace('/tasks'))
        NodeTaskNamespace.node_worker_ref = self

        self.socketIO.connect(
            url=f'{self.server_io.host}:{self.server_io.port}',
            headers=self.server_io.headers,
            wait=False
        )

        # Log the outcome
        i = 0
        while not self.socketIO.connected:
            if i > TIME_LIMIT_INITIAL_CONNECTION_WEBSOCKET:
                self.log.critical('Could not connect to the websocket '
                                  'channels, do you have a slow connection?')
                exit(1)
            self.log.debug('Waiting for socket connection...')
            time.sleep(1)
            i += 1

        self.log.info(f'Connected to host={self.server_io.host} on port='
                      f'{self.server_io.port}')

        self.log.debug("Starting thread for to ping the server to notify this"
                       " node is online.")
        self.socketIO.start_background_task(self.__socket_ping_worker)

    def __socket_ping_worker(self) -> None:
        """
        Send ping messages periodically to the server over the socketIO
        connection to notify the server that this node is online
        """
        # Wait for the socket to be connected to the namespaces on startup
        time.sleep(5)

        while True:
            try:
                self.socketIO.emit('ping', namespace='/tasks')
            except Exception:
                self.log.exception('Ping thread had an exception')
            # Wait before sending next ping
            time.sleep(PING_INTERVAL_SECONDS)

    def get_task_and_add_to_queue(self, task_id: int) -> None:
        """
        Fetches (open) task with task_id from the server. The `task_id` is
        delivered by the websocket-connection.

        Parameters
        ----------
        task_id : int
            Task identifier
        """
        # fetch (open) result for the node with the task_id
        tasks = self.server_io.get_results(
            include_task=True,
            state='open',
            task_id=task_id
        )

        # in the current setup, only a single result for a single node
        # in a task exists.
        for task in tasks:
            self.queue.put(task)

    def run_forever(self) -> None:
        """Keep checking queue for incoming tasks (and execute them)."""
        kill_listener = ContainerKillListener()
        try:
            while True:
                # blocking untill a task comes available
                # timeout specified, else Keyboard interupts are ignored
                self.log.info("Waiting for new tasks....")

                while not kill_listener.kill_now:
                    try:
                        task = self.queue.get(timeout=1)
                        # if no item is returned, the Empty exception is
                        # triggered, thus break statement is not reached
                        break

                    except queue.Empty:
                        pass

                    except Exception as e:
                        self.log.debug(e)

                if kill_listener.kill_now:
                    raise InterruptedError

                # if task comes available, attempt to execute it
                try:
                    self.__start_task(task)
                except Exception as e:
                    self.log.exception(e)

        except (KeyboardInterrupt, InterruptedError):
            self.log.info("Vnode is interrupted, shutting down...")
            self.cleanup()
            sys.exit()

    def kill_containers(self, kill_info: Dict) -> List[Dict]:
        """
        Kill containers on instruction from socket event

        Parameters
        ----------
        kill_info: Dict
            Dictionary received over websocket with instructions for which
            tasks to kill

        Returns
        -------
        List[Dict]:
            List of dictionaries with information on killed task (keys:
            result_id, task_id and parent_id)
        """
        if kill_info['collaboration_id'] != self.server_io.collaboration_id:
            self.log.debug(
                "Not killing tasks as this node is in another collaboration."
            )
            return []
        elif 'node_id' in kill_info and \
                kill_info['node_id'] != self.server_io.whoami.id_:
            self.log.debug(
                "Not killing tasks as instructions to kill tasks were directed"
                " at another node in this collaboration.")
            return []

        # kill specific task if specified, else kill all algorithms
        kill_list = kill_info.get('kill_list')
        killed_algos = self.__docker.kill_tasks(
            org_id=self.server_io.whoami.organization_id, kill_list=kill_list
        )
        # update status of killed tasks
        for killed_algo in killed_algos:
            self.server_io.patch_results(
                id=killed_algo.result_id, result={'status': TaskStatus.KILLED}
            )
        return killed_algos

    def share_node_details(self) -> None:
        """
        Share part of the node's configuration with the server.

        This helps the other parties in a collaboration to see e.g. which
        algorithms they are allowed to run on this node.
        """
        # check if node allows to share node details, otherwise return
        if not self.config.get('share_config', True):
            self.log.debug("Not sharing node configuration in accordance with "
                           "the configuration setting.")
            return

        config_to_share = {}

        encryption_config = self.config.get('encryption')
        if encryption_config:
            if encryption_config.get('enabled') is not None:
                config_to_share['encryption'] = \
                    encryption_config.get('enabled')

        # TODO v4+ remove the old 'allowed_images' key, it's now inside
        # 'policies'. It's now overwritten below if 'policies' is set.
        allowed_algos = self.config.get('allowed_images')
        config_to_share['allowed_algorithms'] = allowed_algos \
            if allowed_algos else 'all'

        # share node policies (e.g. who can run which algorithms)
        policies = self.config.get('policies', {})
        config_to_share['allowed_algorithms'] = \
            policies.get('allowed_algorithms', 'all')
        if policies.get('allowed_users') is not None:
            config_to_share['allowed_users'] = policies.get('allowed_users')
        if policies.get('allowed_organizations') is not None:
            config_to_share['allowed_orgs'] = \
                policies.get('allowed_organizations')

        self.log.debug(f"Sharing node configuration: {config_to_share}")
        self.socketIO.emit(
            'node_info_update', config_to_share, namespace='/tasks'
        )

    def cleanup(self) -> None:

        if hasattr(self, 'socketIO') and self.socketIO:
            self.socketIO.disconnect()
        if hasattr(self, 'vpn_manager') and self.vpn_manager:
            self.vpn_manager.exit_vpn()
        if hasattr(self, 'ssh_tunnels') and self.ssh_tunnels:
            for tunnel in self.ssh_tunnels:
                tunnel.stop()
        if hasattr(self, '_Node__docker') and self.__docker:
            self.__docker.cleanup()

        self.log.info("Bye!")


# ------------------------------------------------------------------------------
def run(ctx):
    """ Start the node."""
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("engineio.client").setLevel(logging.WARNING)

    # initialize node, connect to the server using websockets
    node = Node(ctx)

    # put the node to work, executing tasks that are in the que
    node.run_forever()
