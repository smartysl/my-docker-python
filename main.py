"""
    The main entry point of my-docker based on Python
"""

import argparse

from my_docker.dispatcher import dispatch


def parse_args():
    # type: () -> (str, bool)
    """
    Parse the command line args

    Returns:
        action (str): The command action of my-docker
        tty (bool): Whether to use tty
    """
    parser = argparse.ArgumentParser()

    sub_parsers = parser.add_subparsers(help="my-docker sub actions help")

    parser_run = sub_parsers.add_parser("run", help="run function help")
    parser_run.add_argument(
        "command", help="the command to run"
    )
    parser_run.add_argument(
        "-ti", action="store_true", dest="tty", default=False, help="whether to use tty"
    )
    parser_run.add_argument(
        "-m", dest="memory_limit", help="limitation of memory"
    )
    parser_run.add_argument(
        "-v", "--volume", action="append", dest="volumes", default=[], help="the bound volumes"
    )
    parser_run.add_argument(
        "--name", dest="name", default="", help="the name of container"
    )
    parser_run.add_argument(
        "-e", "--environs", action="append", dest="environs", default=[], help="the additional environ variables"
    )
    parser_run.add_argument(
        "-net", "--network", dest="network_name", help="the network name to connect"
    )
    parser_run.add_argument(
        "-p", "--port", dest="ports", action="append", default=[], help="the port exposed to host"
    )
    parser_run.set_defaults(func=dispatch("run"))

    parser_init = sub_parsers.add_parser("init", help="init function help")
    parser_init.set_defaults(func=dispatch("init"))

    parser_commit = sub_parsers.add_parser("commit", help="commit function help")
    parser_commit.add_argument(
        "image_name", help="the dumped image name"
    )
    parser_commit.set_defaults(func=dispatch("commit"))

    parser_exec = sub_parsers.add_parser("exec", help="exec container help")
    parser_exec.add_argument(
        "--name", required=True, dest="name", help="the container name or uid"
    )
    parser_exec.add_argument(
        "command", help="the command to be executed"
    )
    parser_exec.set_defaults(func=dispatch("exec"))

    parser_stop = sub_parsers.add_parser("stop", help="stop container help")
    parser_stop.add_argument(
        "name", help="the container name or uid to stop"
    )
    parser_stop.set_defaults(func=dispatch("stop"))

    parser_rm = sub_parsers.add_parser("rm", help="rm container help")
    parser_rm.add_argument(
        "name", help="the container name or uid to rm"
    )
    parser_rm.set_defaults(func=dispatch("rm"))

    parser_network_create = sub_parsers.add_parser("network create", help="network create help")
    parser_network_create.add_argument(
        "--subnet", dest="subnet_cidr", help="the cidr of created subnet"
    )
    parser_network_create.add_argument(
        "--driver", dest="driver", help="the driver of created subnet"
    )
    parser_network_create.add_argument(
        "name", help="the name of the created subnet"
    )
    parser_network_create.set_defaults(func=dispatch("network create"))

    parser_network_delete = sub_parsers.add_parser("network delete", help="network delete help")
    parser_network_delete.add_argument(
        "name", help="the name of the subnet to be deleted"
    )
    parser_network_delete.set_defaults(func=dispatch("network delete"))

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    args.func(args)

