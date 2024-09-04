"""
    The common functions for container handlers

"""
import json
import os
import shutil

from .constants import *


def query_container_pid(container_name):
    with open(os.path.join(DEFAULT_INFO_LOCATION.format(container_name), CONFIG_NAME), "r") as f:
        container_info = json.load(f)
        return container_info["pid"]


def update_container_status(container_name, status):
    with open(os.path.join(DEFAULT_INFO_LOCATION.format(container_name), CONFIG_NAME), "r+") as f:
        info = json.load(f)
        info["status"] = status
        json.dump(info, f)


def prepare_work_environment(container_dir):
    os.makedirs(os.path.join(container_dir, WORKER_PATH))
    os.makedirs(os.path.join(container_dir, MNT_PATH))
    os.makedirs(os.path.join(container_dir, UPPER_LAYER_PATH))
    os.makedirs(os.path.join(container_dir, LOWER_LAYER_PATH))
    os.system("tar -xvf /root/busybox.tar -C {} > /dev/null".format(os.path.join(container_dir, LOWER_LAYER_PATH)))
    os.system("mount -t overlay overlay -o lowerdir={},upperdir={},workdir={} {}".format(os.path.join(container_dir, LOWER_LAYER_PATH),
                                                                                         os.path.join(container_dir, UPPER_LAYER_PATH),
                                                                                         os.path.join(container_dir, WORKER_PATH),
                                                                                         os.path.join(container_dir, MNT_PATH)))


def clean_work_environment(container_dir):
    os.system(f"umount {os.path.join(container_dir, MNT_PATH)}")

    shutil.rmtree(container_dir)
