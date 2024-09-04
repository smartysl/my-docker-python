"""
    The manager class of cgroups

"""
from .memory import Memory


subsystems = [Memory()]


class CgroupManager:
    def __init__(self, container_name, cgroup_config=None):
        self.path = f"{container_name}-cgroup"
        self.cgroup_config = cgroup_config

    def apply(self, pid):
        for subsystem in subsystems:
            subsystem.apply(self.path, pid)

    def set(self):
        for subsystem in subsystems:
            subsystem.set(self.path, self.cgroup_config)

    def remove(self):
        for subsystem in subsystems:
            subsystem.remove(self.path)
