from subprocess import call
import subprocess
import logging
import datetime
import os
import time
from subprocess import Popen, PIPE, STDOUT
import re

# sensitivity of silence recognition
threshold = '10%'

if  __name__ == "__main__":
    logging.basicConfig(filename='sound.log', format='%(filename)s [%(lineno)d] %(message)s',
                        level=logging.INFO)

    #value = [];

    while (True):

        

        start_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        start_time = datetime.datetime.now()
        start = start_time.strftime('%Y-%m-%d %H:%M:%S')
        output_filename = 'rec.wav'

    
        cmd = ['rec', '-c', '2', output_filename, 'rate', '8k', 'trim', '0', '10']
        call(cmd)

        os.rename("rec.wav", "/home/pi/OnoSW/data/opsoroassistant/rec.wav")

        end_time = datetime.datetime.now()
        end = end_time.strftime('%Y-%m-%d %H:%M:%S')
        logging.info("%s ~ %s (%f)" %(start, end,(end_time-start_time).total_seconds()))
        time.sleep(1)


        output = subprocess.check_output("sox /home/pi/OnoSW/data/opsoroassistant/rec.wav -n stat 2>&1 | grep 'RMS     amplitude:'",stderr= subprocess.STDOUT, shell=True)
        value = output.split('     ')[2]
        
        value = float(value)
        value = value * 10000
        print value
        if(value < 100):
             print 'stil'
        else:
            print 'luid'
        
       

        time.sleep(5)
