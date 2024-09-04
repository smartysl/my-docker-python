import subprocess
import sys
import os

os.execve()

CGROUP_MEMORY_HIERARCHY_MOUNT = "/sys/fs/cgroup/memory"


def cgroup_limit(pid):
    limit_cgroup_path = os.path.join(CGROUP_MEMORY_HIERARCHY_MOUNT, "test-memory-limit")

    if not os.path.isdir(limit_cgroup_path):
        os.makedirs(limit_cgroup_path)

    with open(os.path.join(limit_cgroup_path, "tasks"), "a") as f:
        f.write(str(pid))

    with open(os.path.join(limit_cgroup_path, "memory.limit_in_bytes"), "a") as f:
        f.write("100m")


def exec_command(proc, command):
    proc.stdin.write(f"{command}\n".encode())
    proc.stdin.flush()


def unshare():
    command = ["unshare", "-i", "-m", "-n", "-p", "-U", "-f", "--propagation=private"]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=sys.stdout)

    print("Proc pid is {}".format(proc.pid))
    cgroup_limit(proc.pid)
    exec_command(proc, "stress-ng --vm-bytes 200m --vm-keep -m 1")

    proc.wait()


if __name__ == '__main__':
    unshare()