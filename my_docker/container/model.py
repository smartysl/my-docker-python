"""
    The models of mydocker container

"""
from enum import Enum


class ContainerStatus(Enum):
    RUNNING = "running"
    STOP = "stopped"
    EXIT = "exited"


class ContainerInfo:
    def __init__(self, pid, uid, name, command, created_time, status, ports):
        self.pid = pid
        self.uid = uid
        self.name = name
        self.command = command
        self.create_time = created_time
        self.status = status
        self.ports = ports
