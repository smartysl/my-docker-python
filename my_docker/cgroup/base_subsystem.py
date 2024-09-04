"""
    Base class for subsystem

"""
import abc


class CGroupConfig:
    def __init__(self):
        self.memory_limit = ""

    @classmethod
    def build(cls, args):
        config = CGroupConfig()
        for k, v in vars(args).items():
            if getattr(config, k, None) is not None:
                setattr(config, k, v)
        return config


class BaseSubSystem(metaclass=abc.ABCMeta):
    name = abc.abstractproperty()

    @abc.abstractmethod
    def set(self, cgroup_path, cgroup_config):
        pass

    @abc.abstractmethod
    def remove(self, cgroup_path):
        pass

    @abc.abstractmethod
    def apply(self, cgroup_path, pid):
        pass
