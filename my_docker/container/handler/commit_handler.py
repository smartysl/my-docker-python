"""
    The handler of run action
"""
import os
import json

from ..constants import *


def handle_commit(args):
    image_tar = os.path.join("/root", args.image_name + ".tar")
    os.system(f"tar -czf {image_tar} -C {MNT_PATH} .")
