"""
    The handler of run action
"""
import os
import json

from ctypes import CDLL, c_int

from ..container_manager import query_container_pid


def handle_exec(args):
    enter = CDLL("my_docker/ns_enter/nsenter.so")
    pid = c_int(query_container_pid(args.name))
    enter.enter_namespace(pid)

    split_command = args.command.split()
    os.execvp(split_command[0], split_command)

