"""
    The handler for create network command
"""
from ..network_model import Network


def handle_create(args):
    Network.create_network(args.driver, args.subnet_cidr, args.name)


action_dispatcher = {
    "create": handle_create
}


def handle_action(args):
    action = args.action
    func = action_dispatcher[action]
    func(args)
