from subprocess import call
from subprocess import Popen, PIPE, STDOUT
import subprocess
import logging
import datetime
import os
import time
import sys



#call(['sox', '/home/pi/OnoSW/data/opsoroassistant/rec.wav', '-n', 'stat', '2>&1', '|', 'sed', '-n', 's#^RMS     amplitude:[^0-9]*\([0-9.]*\)$#\1#p'], shell=True)

output = subprocess.check_output(["sox /home/pi/OnoSW/data/opsoroassistant/rec.wav -n stat 2>&1 | sed -n 's#^RMS     amplitude:[^0-9]*\([0-9.]*\)$#\1#p'"],stderr= subprocess.STDOUT, shell=True)
print 'Have %d bytes in output' % len(output)
print output


