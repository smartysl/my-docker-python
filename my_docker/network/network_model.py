"""
    The models of network
"""
import json
import os
import uuid

from .constants import *
from .ipam import IPAM


class Network:
    ipam = IPAM(SUBNET_ALLOCATOR_DIR)

    networks_dump_file = os.path.join(SUBNET_ALLOCATOR_DIR, "networks.json")

    def __init__(self, name, subnet_cidr, gateway_ip, driver_name):
        self.name = name
        self.subnet_cidr = subnet_cidr
        self.gateway_ip = gateway_ip
        self.driver_name = driver_name

    def dump(self):
        if not os.path.isfile(self.networks_dump_file):
            with open(self.networks_dump_file, "w") as f:
                json.dump({}, f)

        with open(self.networks_dump_file, "r") as f:
            networks = json.load(f)
        networks[self.name] = vars(self)
        with open(self.networks_dump_file, "w") as f:
            json.dump(networks, f)

    def delete(self):
        from .drivers import drivers

        drivers[self.driver_name].delete(self)

        with open(self.networks_dump_file, "r") as f:
            networks = json.load(f)
        del networks[self.name]
        with open(self.networks_dump_file, "w") as f:
            json.dump(networks, f)

    @classmethod
    def load(cls, name):
        with open(cls.networks_dump_file, "r") as f:
            networks = json.load(f)
            return cls(**networks[name])

    @classmethod
    def create_network(cls, driver_name, subnet_cidr, name):
        from .drivers import drivers

        default_gateway_ip = cls.ipam.allocate(subnet_cidr) + "/" + subnet_cidr.split("/")[1]
        network = drivers[driver_name].create(subnet_cidr, default_gateway_ip, name)
        network.dump()

    def connect(self, container_info):
        from .drivers import drivers

        endpoint = Endpoint.create(container_info, self)
        drivers[self.driver_name].connect(self, endpoint)

    def disconnect(self, container_name):
        from .drivers import drivers

        endpoint = Endpoint.load(container_name)
        drivers[self.driver_name].disconnect(self, endpoint)
        endpoint.delete(self)


class Endpoint:
    ipam = IPAM(SUBNET_ALLOCATOR_DIR)

    endpoints_dump_file = os.path.join(SUBNET_ALLOCATOR_DIR, "endpoints.json")

    def __init__(self, uid, container_name, container_pid, device,
                 ip_address, mac_address=None, port_mapping=None):
        self.uid = uid
        self.container_name = container_name
        self.container_pid = container_pid
        self.device = device
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.port_mapping = port_mapping

    @classmethod
    def create(cls, container_info, network):
        uid = str(uuid.uuid1())
        device = [f"veth0-{uid[:5]}", f"veth1-{uid[:5]}"]
        ip_address = cls.ipam.allocate(network.subnet_cidr) + "/" + network.subnet_cidr.split("/")[1]

        endpoint = cls(uid=uid, container_name=container_info.name, container_pid=container_info.pid,
                       device=device, ip_address=ip_address, port_mapping=container_info.ports)
        endpoint.dump()
        return endpoint

    @classmethod
    def load(cls, container_name):
        with open(cls.endpoints_dump_file, "r") as f:
            endpoints = json.load(f)
            return cls(**endpoints[container_name])

    def dump(self):
        if not os.path.isfile(self.endpoints_dump_file):
            with open(self.endpoints_dump_file, "w") as f:
                json.dump({}, f)

        with open(self.endpoints_dump_file, "r") as f:
            endpoints = json.load(f)

        endpoints[self.container_name] = vars(self)

        with open(self.endpoints_dump_file, "w") as f:
            json.dump(endpoints, f)

    def delete(self, network):
        self.ipam.release(network.subnet_cidr, self.ip_address.split("/")[0])

        with open(self.endpoints_dump_file, "r") as f:
            endpoints = json.load(f)

        del endpoints[self.container_name]
        with open(self.endpoints_dump_file, "w") as f:
            json.dump(endpoints, f)
