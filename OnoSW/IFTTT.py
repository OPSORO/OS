from azure.servicebus import ServiceBusService , Message , Queue
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc
from __future__ import print_function

import threading
import subprocess
import requests

headers = {
    'Content-Type': 'application/json'
}


sched= BlockingScheduler(timezone=utc)

	

AZURE_SERVICEBUS_NAMESPACE='oassistant'
AZURE_SERVICEBUS_ISSUER='RootManageSharedAccessKey'
AZURE_SERVICEBUS_ACCOUNT_KEY='ma3ulhX5/kvLijAcgKC4MS58NT5etxbw0WPGJnbobqs='

bus_service = ServiceBusService(
	service_namespace=AZURE_SERVICEBUS_NAMESPACE,
	shared_access_key_name=AZURE_SERVICEBUS_ISSUER,
	shared_access_key_value=AZURE_SERVICEBUS_ACCOUNT_KEY
			)

def GetCalenderMessages():
	CalenderMessage = bus_service.receive_queue_message('calendar', peek_lock=True)
	#requests.post('http://172.23.36.28/app/assistant/saytts')
	if CalenderMessage != None:
		message = str(CalenderMessage.body)
		queuemessage = message.split('|')[1]
		file = open("queuemessage","w")
		file.write(queuemessage)
		file.close()
		
		#print(r.status_code)
		CalenderMessage.delete()




def GetNewsMessages():
	NewsMessage  = bus_service.receive_queue_message('news', peek_lock=True)
	if NewsMessage != None:
		message = str(NewsMessage.body)
		queuemessage = message.split('|')[1]
		print(queuemessage)
		NewsMessage.delete()


def GetWeatherMessages():
	WeatherMessage  = bus_service.receive_queue_message('weather', peek_lock=True)
	if WeatherMessage != None:
		message = str(WeatherMessage.body)
		queuemessage = message.split('|')[1]
		print(queuemessage)
		WeatherMessage.delete()

threading.Timer(1.0, GetCalenderMessages).start()

sched= BlockingScheduler(timezone=utc)
sched.add_job(GetCalenderMessages,'interval',id="calendarmessage_job",seconds=1 )
sched.add_job(GetNewsMessages,'interval', id='newsmessage_job',minutes=1)
sched.add_job(GetWeatherMessages,'cron',day_of_week='mon-sun',hour=10,minute=5)
sched.start()