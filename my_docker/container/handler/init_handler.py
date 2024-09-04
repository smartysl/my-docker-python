"""
    The handler of run action
"""
import json
import os

from ..constants import *


def handle_init(args):
    execution_params = json.loads(os.read(3, 4096).decode())
    os.close(3)
    split_command = execution_params["command"].split()
    volumes = execution_params["volumes"]
    container_name = execution_params["container_name"]

    mnt_path = os.path.join(DEFAULT_LAYER_LOCATION.format(container_name), MNT_PATH)

    os.system(f"mount --rbind {mnt_path} {mnt_path}")

    # mount volumes
    for volume in volumes:
        host_dir, container_dir = volume.split(":")[0], mnt_path + volume.split(":")[1]
        if not os.path.isdir(host_dir):
            os.mkdir(host_dir)
        if not os.path.isdir(container_dir):
            os.mkdir(container_dir)
        os.system(f"mount --rbind {host_dir} {container_dir}")

    os.mkdir(os.path.join(mnt_path, ".pivot_root"))
    os.system(f"pivot_root {mnt_path} {os.path.join(mnt_path, '.pivot_root')}")
    os.chdir("/")

    os.system("mount --make-rprivate /")
    os.system("mount -t proc proc /proc")

    os.execvp(split_command[0], split_command)

