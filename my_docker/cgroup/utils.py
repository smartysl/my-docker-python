"""
    The utils for cgroup management

"""
import os


def find_cgroup_mount_point(subsystem_name):
    with open("/proc/self/mountinfo", "r") as f:
        mount_info = f.readlines()

    for line in mount_info:
        split_line = line.split()
        if split_line[-2] == "cgroup" and split_line[-3] == "cgroup":
            if split_line[-1].split(",")[1] == subsystem_name:
                return split_line[4]
    raise ValueError("cgroup mount point not found")


def get_cgroup_path(subsystem_name, cgroup_path):
    cgroup_root = find_cgroup_mount_point(subsystem_name)
    cgroup_dir = os.path.join(cgroup_root, cgroup_path)
    if not os.path.isdir(cgroup_dir):
        os.mkdir(cgroup_dir)
    return cgroup_dir
