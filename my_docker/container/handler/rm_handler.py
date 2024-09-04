"""
    The handler of rm container
"""
import os
import signal
import shutil

from my_docker.cgroup.cgroup_manager import CgroupManager

from ..container_manager import clean_work_environment
from ..model import ContainerStatus
from ..constants import DEFAULT_LAYER_LOCATION, DEFAULT_INFO_LOCATION

from ...network.network_model import Network

def handler_rm(args):
    clean_work_environment(DEFAULT_LAYER_LOCATION.format(args.name))

    CgroupManager(args.name).remove()

    shutil.rmtree(DEFAULT_INFO_LOCATION.format(args.name))

    network = Network.load(args.network_name)
    network.disconnect(args.name)
