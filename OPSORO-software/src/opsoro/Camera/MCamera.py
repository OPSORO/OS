import os
import os.path
import subprocess, signal
from opsoro.console_msg import *

class _MCamera(object):
    """docstring for _camera_motion."""
    def __init__(self):
        super(_MCamera, self).__init__()

    def start(self):
        devnull = open('/dev/null', 'w')
        proc = subprocess.Popen(["motion"], stdout=subprocess.PIPE, stderr=devnull)
        print_info("Motion server on")
        #os.system("motion")



    def stop(self):
        proc = subprocess.Popen(["pgrep", "motion"], stdout=subprocess.PIPE)

        # Kill process.
        for pid in proc.stdout:
            os.kill(int(pid), signal.SIGTERM)
            # Check if the process that we killed is alive.
            if os.path.exists("/proc/" + str(pid)):
                print_info("Wasn't able to kill the motion process. HINT:use signal.SIGKILL or signal.SIGABORT")
            else:
                print_info("Motion server off")

MCamera = _MCamera()
