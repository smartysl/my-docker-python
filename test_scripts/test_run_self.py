import subprocess
import os
import sys
import time

from multiprocessing import Process

if __name__ == '__main__':
    if sys.argv[1] == "read":
        print(os.read(3, 1000))
        exit(0)


    r, w = os.pipe()

    proc = subprocess.Popen(["python", "test_run_self.py", "read"], pass_fds=[r], close_fds=True)
    print(os.getpid())
    print(proc.pid)
    proc.wait()