"""
    The bridge driver class
"""
import os

from .network_model import Network
from .base_network_driver import NetworkDriver


class BridgeDriver(NetworkDriver):
    name = "bridge"

    def create(self, subnet_cidr, default_gateway_ip, name):
        os.system(f"brctl addbr {name}")

        os.system(f"ip addr add {default_gateway_ip} dev {name}")

        os.system(f"ip link set dev {name} up")

        os.system(f"iptables -t nat -A POSTROUTING -s {subnet_cidr} ! -o {name} -j MASQUERADE")

        return Network(name=name, subnet_cidr=subnet_cidr,
                       gateway_ip=default_gateway_ip, driver_name=self.name)

    def delete(self, network):
        os.system(f"ip link set dev {network.name} down")

        os.system(f"brctl delbr {network.name}")

        result = os.popen(f"iptables -t nat -vnL POSTROUTING --line-number | grep \"\!{network.name}\"").read()
        rule_number = result.split()[0]
        os.system(f"iptables -t nat -D POSTROUTING {rule_number}")

    def connect(self, network, endpoint):
        os.system(f"ip link add {endpoint.device[0]} type veth peer name {endpoint.device[1]}")

        os.system(f"ip link set dev {endpoint.device[0]} up")

        os.system(f"brctl addif {network.name} {endpoint.device[0]}")

        os.system(f"ip link set {endpoint.device[1]} netns {endpoint.container_pid}")

        os.system(
            f"nsenter --net=/proc/{endpoint.container_pid}/ns/net ip link set {endpoint.device[1]} up")

        os.system(f"nsenter --net=/proc/{endpoint.container_pid}/ns/net ip addr add {endpoint.ip_address} dev {endpoint.device[1]}")

        os.system(f"nsenter --net=/proc/{endpoint.container_pid}/ns/net ip route add {network.subnet_cidr} dev {endpoint.device[1]}")

        os.system(f"nsenter --net=/proc/{endpoint.container_pid}/ns/net ip route add default via {network.gateway_ip.split('/')[0]}")

        for item in endpoint.port_mapping:
            host_port, inside_port = item.split(":")
            os.system(f"iptables -t nat -A PREROUTING -p tcp -m tcp --dport {host_port} -j DNAT --to-destination {endpoint.ip_address.split('/')[0]}:{inside_port}")

    def disconnect(self, network, endpoint):
        for item in endpoint.port_mapping:
            host_port, _ = item.split(":")
            result = os.popen(f"iptables -t nat -vnL PREROUTING --line-number | grep \"dpt:{host_port}\"").read()
            rule_number = result.split()[0]
            os.system(f"iptables -t nat -D PREROUTING {rule_number}")