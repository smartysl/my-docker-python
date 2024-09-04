"""
    The delete handler of network
"""
from ..network_model import Network


def handle_delete(args):
    network = Network.load(args.name)

    network.delete()
