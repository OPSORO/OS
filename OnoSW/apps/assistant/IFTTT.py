# from __future__ import print_function
# from azure.servicebus import ServiceBusService , Message , Queue
# from apscheduler.schedulers.blocking import BlockingScheduler
# from pytz import utc
# # from sound import Sound

# import threading
# import subprocess
# import requests

# headers = {
#     'Content-Type': 'application/json'
# }


# sched= BlockingScheduler(timezone=utc)

	

# AZURE_SERVICEBUS_NAMESPACE='oassistant'
# AZURE_SERVICEBUS_ISSUER='RootManageSharedAccessKey'
# AZURE_SERVICEBUS_ACCOUNT_KEY='ma3ulhX5/kvLijAcgKC4MS58NT5etxbw0WPGJnbobqs='

# bus_service = ServiceBusService(
# 	service_namespace=AZURE_SERVICEBUS_NAMESPACE,
# 	shared_access_key_name=AZURE_SERVICEBUS_ISSUER,
# 	shared_access_key_value=AZURE_SERVICEBUS_ACCOUNT_KEY
# 			)

# def GetCalenderMessages():
# 	CalenderMessage = bus_service.receive_queue_message('calendar', peek_lock=True)
# 	if CalenderMessage != None:
# 		message = str(CalenderMessage.body)
# 		queuemessage = message.split('|')[1]
# 		print(queuemessage)		
# 		CalenderMessage.delete()




# def GetNewsMessages():
# 	NewsMessage  = bus_service.receive_queue_message('news', peek_lock=True)
	if NewsMessage != None:
		message = str(NewsMessage.body)
		queuemessage = message.split('|')[1]
		print(queuemessage)
		NewsMessage.delete()


# def GetWeatherMessages():
# 	WeatherMessage  = bus_service.receive_queue_message('weather', peek_lock=True)
# 	if WeatherMessage != None:
# 		message = str(WeatherMessage.body)
# 		queuemessage = message.split('|')[1]
# 		print(queuemessage)
# 		WeatherMessage.delete()

# # threading.Timer(1.0, GetCalenderMessages).start()

# sched= BlockingScheduler(timezone=utc)
# sched.add_job(GetCalenderMessages,'interval',id="calendarmessage_job",seconds=1 )
# sched.add_job(GetNewsMessages,'interval', id='newsmessage_job',minutes=1)
# sched.add_job(GetWeatherMessages,'cron',day_of_week='mon-sun',hour=10,minute=5)
# sched.start()
from azure.servicebus import ServiceBusService , Message , Queue
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc


import subprocess
import requests
from subprocess import call
import subprocess
import logging
import datetime
import os
import time
from subprocess import Popen, PIPE, STDOUT
import re


sched= BlockingScheduler(timezone=utc)

	

AZURE_SERVICEBUS_NAMESPACE='oassistant'
AZURE_SERVICEBUS_ISSUER='RootManageSharedAccessKey'
AZURE_SERVICEBUS_ACCOUNT_KEY='ma3ulhX5/kvLijAcgKC4MS58NT5etxbw0WPGJnbobqs='

bus_service = ServiceBusService(
	service_namespace=AZURE_SERVICEBUS_NAMESPACE,
	shared_access_key_name=AZURE_SERVICEBUS_ISSUER,
	shared_access_key_value=AZURE_SERVICEBUS_ACCOUNT_KEY
			)



if  __name__ == "__main__":
    logging.basicConfig(filename='sound.log', format='%(filename)s [%(lineno)d] %(message)s',
                        level=logging.INFO)

    #value = [];


def record():
    while (True):

        

        start_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        start_time = datetime.datetime.now()
        start = start_time.strftime('%Y-%m-%d %H:%M:%S')
        output_filename = 'rec.wav'

    
        cmd = ['rec', '-c', '2', output_filename, 'rate', '8k', 'trim', '0', '10']
        call(cmd)

        os.rename("rec.wav", "/home/pi/OnoSW/data/assistant/rec.wav")

        end_time = datetime.datetime.now()
        end = end_time.strftime('%Y-%m-%d %H:%M:%S')
        logging.info("%s ~ %s (%f)" %(start, end,(end_time-start_time).total_seconds()))
        time.sleep(1)


        output = subprocess.check_output("sox /home/pi/OnoSW/data/assistant/rec.wav -n stat 2>&1 | grep 'RMS     amplitude:'",stderr= subprocess.STDOUT, shell=True)
        value = output.split('     ')[2]
        
        value = float(value)
        value = value * 10000
        print value
        if(value < 100):
            print("stil")
            payload={'subject':'NEWS'}
			r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload)
			if r != None:
				r= str(r.text)
				message=r.split('|')[1]
				print(message)
    #         def GetCalenderMessages():
				# payload={'subject':'CALENDER'}
				# r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload)
				# if r != None:
				# 	r= str(r.text)
				# 	message=r.split('|')[1]
				# 	print(message)
				# 	record()


    #         def GetNewsMessages():
				# payload={'subject':'NEWS'}
				# r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload)
				# if r != None:
				# 	r= str(r.text)
				# 	message=r.split('|')[1]
				# 	print(message)
				# 	record()


    #         def GetWeatherMessages():
				# payload={'subject':'WEATHER'}
				# r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload)
				# if r != None:
				# 	r= str(r.text)
				# 	message=r.split('|')[1]
				# 	print(message)
				# 	record()

        #     sched= BlockingScheduler(timezone=utc)
        #     sched.add_job(GetCalenderMessages,'interval',id="calendarmessage_job",seconds=1)
        #     sched.add_job(GetNewsMessages,'interval', id='newsmessage_job',seconds=10)
        #     sched.add_job(GetWeatherMessages,'cron',day_of_week='mon-sun',hour=10,minute=5)
        #     sched.start()
        #     time.sleep(10)
            
        # else:
        #     print("luid")
    #         def GetCalenderMessages():
				# payload={'subject':'CALENDER'}
				# r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload)
				# if r != None:
				# 	r= str(r.text)
				# 	message=r.split('|')[1]
				# 	print(message)
				# 	record()

    #         sched= BlockingScheduler(timezone=utc)
    #         sched.add_job(GetCalenderMessages,'interval',id="calendarmessage_job",seconds=1)
    #         sched.start()
#             time.sleep(10)
            
#         time.sleep(5)
# record()