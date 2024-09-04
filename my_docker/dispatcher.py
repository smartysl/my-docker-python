"""
    The dispatcher for actions of my-docker
"""

from my_docker.container.handler.run_handler import handle_run
from my_docker.container.handler.init_handler import handle_init
from my_docker.container.handler.commit_handler import handle_commit
from my_docker.container.handler.exec_handler import handle_exec
from my_docker.container.handler.stop_handler import handle_stop
from my_docker.container.handler.rm_handler import handler_rm

from my_docker.network.handler.create_handler import handle_create
from my_docker.network.handler.delete_handler import handle_delete


def dispatch(action):
    # type: (str) -> function
    """
    Dispatch the action to particular handler
    """
    dispatch_map = {
        "run": handle_run,
        "init": handle_init,
        "commit": handle_commit,
        "exec": handle_exec,
        "stop": handle_stop,
        "rm": handler_rm,
        "network create": handle_create,
        "network delete": handle_delete
    }
    return dispatch_map[action]
