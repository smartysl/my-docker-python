"""
    The common functions for container handlers

"""
import json
import os

from .constants import *


def query_container_pid(container_name):
    with open(os.path.join(DEFAULT_INFO_LOCATION.format(container_name), CONFIG_NAME), "r") as f:
        container_info = json.load(f)
        return container_info["pid"]


def update_container_status(container_name, status):
    with open(os.path.join(DEFAULT_INFO_LOCATION.format(container_name), CONFIG_NAME), "w+") as f:
        info = json.load(f)
        info["status"] = status
        json.dump(info, f)
