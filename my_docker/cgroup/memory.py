"""
    The implementation of cgroup memory limit

"""
import os

from .base_subsystem import BaseSubSystem
from .utils import get_cgroup_path


class Memory(BaseSubSystem):
    name = "memory"

    def set(self, cgroup_path, cgroup_config):
        if not cgroup_config.memory_limit:
            return
        with open(os.path.join(get_cgroup_path(self.name, cgroup_path), "memory.limit_in_bytes"), "a") as f:
            f.write(cgroup_config.memory_limit)

    def remove(self, cgroup_path):
        os.rmdir(os.path.join(get_cgroup_path(self.name, cgroup_path)))

    def apply(self, cgroup_path, pid):
        with open(os.path.join(get_cgroup_path(self.name, cgroup_path), "tasks"), "a") as f:
            f.write(str(pid))