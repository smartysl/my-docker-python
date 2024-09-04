"""
    The handler of run action
"""

import json
import os
import shutil
import subprocess
import sys
import random
import time
import traceback

from datetime import datetime

from my_docker.cgroup.base_subsystem import CGroupConfig
from my_docker.cgroup.cgroup_manager import CgroupManager
from ..constants import *
from ..model import ContainerInfo, ContainerStatus
from ..container_manager import prepare_work_environment, clean_work_environment
from ...network.network_model import Network, Endpoint


def generate_container_uid(container_name):
    random.seed(time.time_ns())
    uid = "".join([str(random.randint(0, 10)) for _ in range(10)])
    if not container_name:
        container_name = uid
    return container_name, uid


def record_container_info(pid, command, container_name, uid, ports):
    container_info = ContainerInfo(pid=pid, uid=uid, name=container_name,
                                   command=command, status=ContainerStatus.RUNNING.value,
                                   created_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   ports=ports)
    container_dir = DEFAULT_INFO_LOCATION.format(container_name)
    with open(os.path.join(container_dir, CONFIG_NAME), "w") as f:
        json.dump(vars(container_info), f)
    return container_info


def handle_run(args):
    print(f"Father Pid is {os.getpid()}")

    container_name, uid = generate_container_uid(args.name)
    os.makedirs(DEFAULT_INFO_LOCATION.format(container_name))

    cgroup_manager = CgroupManager(container_name, CGroupConfig.build(args))

    prepare_work_environment(DEFAULT_LAYER_LOCATION.format(container_name))

    container_environ_variables = dict(os.environ)
    for environ in args.environs:
        container_environ_variables[environ.split("=")[0]] = environ.split("=")[1]

    r, w = os.pipe()

    if args.tty:
        stdout = sys.stdout
    else:
        stdout = open(os.path.join(DEFAULT_INFO_LOCATION.format(container_name), "container.log"), "w")

    try:
        command = ["unshare", "-i", "-m", "-n", "-p", "-U", "-f", "-r", "python", "main.py", "init"]
        proc = subprocess.Popen(command, stdin=sys.stdin, stdout=stdout,
                                stderr=sys.stderr, pass_fds=[r], close_fds=True,
                                preexec_fn=os.setsid, env=container_environ_variables)
        print(f"Child Pid is {proc.pid}")
        print(f"Container name is {container_name}")

        container_info = record_container_info(proc.pid, args.command,
                                               container_name, uid, args.ports)

        # set cgroup
        cgroup_manager.set()
        cgroup_manager.apply(proc.pid)

        try:
            # set network
            network = Network.load(args.network_name)
            network.connect(container_info)
        except Exception:
            traceback.print_exc()

        # send execution params to subprocess through pipe
        execution_params = {
            "command": args.command,
            "volumes": args.volumes,
            "container_name": container_name
        }
        os.write(w, json.dumps(execution_params).encode())
        os.close(w)

        if args.tty:
            proc.wait()
    finally:
        if args.tty:
            # clean the cgroup dir
            cgroup_manager.remove()

            # clean the container layers
            clean_work_environment(DEFAULT_LAYER_LOCATION.format(container_name))

            # clean the container config
            shutil.rmtree(DEFAULT_INFO_LOCATION.format(container_name))
