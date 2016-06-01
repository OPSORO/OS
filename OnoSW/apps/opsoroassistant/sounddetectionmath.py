from subprocess import call
import logging
import datetime
import os.path
import time

# sensitivity of silence recognition
threshold = '10%'

if  __name__ == "__main__":
    logging.basicConfig(filename='sound.log', format='%(filename)s [%(lineno)d] %(message)s',
                        level=logging.INFO)
    while (True):
        start_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        start_time = datetime.datetime.now()
        start = start_time.strftime('%Y-%m-%d %H:%M:%S')
        output_filename = 'rec.wav'

        cmd = ['rec', '-c', '2', output_filename, 'rate', '8k', 'silence', '1', '0.1', threshold, '1', '3.0', threshold]

        call(cmd)

        os.rename("rec.wav", "/home/pi/OnoSW/data/opsoroassistant/rec.wav")

        end_time = datetime.datetime.now()
        end = end_time.strftime('%Y-%m-%d %H:%M:%S')
        logging.info("%s ~ %s (%f)" %(start, end,(end_time-start_time).total_seconds()))
        time.sleep(10)