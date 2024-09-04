"""
    The IPAM allocate class
"""
import os
import json


def ip2int(ip):
    ret = 0
    reversed_ip = ip.split(".")[::-1]
    for i in range(4):
        ret += int(reversed_ip[i]) * (256 ** i)
    return ret


def int2ip(int_ip):
    ret = []
    for i in range(4):
        pos = i * 8
        ret.append(str((int_ip & (255 << pos)) >> pos))
    return ".".join(ret[::-1])


class IPAM:
    def __init__(self, subnet_allocator_dir):
        self.subnet_path = os.path.join(subnet_allocator_dir, "subnets.json")

        if not os.path.isdir(subnet_allocator_dir):
            os.makedirs(subnet_allocator_dir)
            with open(self.subnet_path, "w") as f:
                json.dump({}, f)

    def load(self, subnet_cidr):
        with open(self.subnet_path, "r") as f:
            subnets = json.load(f)
            if subnet_cidr in subnets:
                return subnet_cidr, subnets[subnet_cidr]
            else:
                return None, None

    def store(self, subnet_cidr, allocated):
        with open(self.subnet_path, "r") as f:
            subnets = json.load(f)

        with open(self.subnet_path, "w") as f:
            subnets[subnet_cidr] = allocated
            json.dump(subnets, f)

    def allocate(self, subnet_cidr):
        subnet, mask = subnet_cidr.split("/")

        _, allocated = self.load(subnet_cidr)
        if not allocated:
            allocated = 1 << (2 ** (32 - int(mask)))
        n = 0
        while (allocated >> n) & 1 != 0:
            n += 1
        if n >= 2 ** (32 - int(mask)):
            print("All ips in this subnet are allocated")
            return ""

        allocated ^= 1 << n
        int_ip = ip2int(subnet) + n + 1
        allocated_ip = int2ip(int_ip)
        self.store(subnet_cidr, allocated)
        return allocated_ip

    def release(self, subnet_cidr, ip_address):
        subnet, _ = subnet_cidr.split("/")
        _, allocated = self.load(subnet_cidr)

        allocated ^= 1 << (ip2int(ip_address) - ip2int(subnet) - 1)
        self.store(subnet_cidr, allocated)


if __name__ == '__main__':
    ipam = IPAM("/root/mydocker/network")
    for _ in range(4):
        print(ipam.allocate("192.168.0.0/27"))
    ipam.release("192.168.0.0/27", "192.168.0.1")
    ipam.release("192.168.0.0/27", "192.168.0.3")
    for _ in range(4):
        print(ipam.allocate("192.168.0.0/27"))

