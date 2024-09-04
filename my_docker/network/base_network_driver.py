"""
    The base class of network driver
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class NetworkDriver(metaclass=ABCMeta):
    name = abstractproperty

    @abstractmethod
    def create(self, subnet_cidr, default_gateway_ip, name):
        pass

    @abstractmethod
    def delete(self, network):
        pass

    @abstractmethod
    def connect(self, network, endpoint):
        pass

    @abstractmethod
    def disconnect(self, network, endpoint):
        pass
