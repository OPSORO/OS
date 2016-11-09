import time
import sys
import imp
sys.path.append('../opsoro/')
from hardware import Hardware

loop = True
with Hardware.lock:
    Hardware.servo_init()
    Hardware.servo_enable()
while(loop):
    Hardware.servo_set(0,1500)
    Hardware.servo_set(1,0)
    time.sleep(1)
