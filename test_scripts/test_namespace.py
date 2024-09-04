import subprocess
import sys


def unshare():
    command = ["unshare", "-i", "-m", "-n", "-p", "-U", "-f", "--propagation=private"]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=sys.stdout)
    proc.stdin = sys.stdin
    # proc.stdin = sys.stdin
    # proc.stdout = sys.stdout
    proc.wait()


if __name__ == '__main__':
    unshare()