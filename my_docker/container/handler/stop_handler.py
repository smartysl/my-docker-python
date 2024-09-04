"""
    The handler of stop container action
"""
import os
import signal

from ..container_manager import query_container_pid, update_container_status
from ..model import ContainerStatus


def handle_stop(args):
    pid = query_container_pid(args.name)

    os.killpg(pid, signal.SIGKILL)
    print(args.name)

    update_container_status(args.name, ContainerStatus.STOP.value)




