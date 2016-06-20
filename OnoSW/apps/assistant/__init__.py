from __future__ import print_function
from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename
from sound import Sound
from subprocess import Popen, PIPE, STDOUT
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import imp
import requests

#import for recording from ifttt.py
from pytz import utc


import subprocess
import requests
from subprocess import call
import subprocess
import logging
import datetime
import os
import sys
import time
from subprocess import Popen, PIPE, STDOUT
import re

#end import

import math
import cmath

from console_msg import *
from hardware import Hardware
from stoppable_thread import StoppableThread

from functools import partial
from exceptions import RuntimeError
import os
import glob
import shutil
import time
import yaml
import subprocess
# import IFTTT



from subprocess import call
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader

from flask import Blueprint, render_template, request, send_from_directory

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

from expression import Expression

config = {"full_name": "Assistant", "icon": "fa-calendar"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


# def AppLoop():
# 	while not app_t.stopped():
# 		with Expression.lock:
# 			Expression.update()
#
# 		app_t.sleep(0.015)
#
# app_t = None

def setup_pages(opsoroapp):
	app_bp = Blueprint("assistant", __name__, template_folder="templates", static_folder="static")

	@app_bp.route("/", methods=["GET"])
	@opsoroapp.app_view
	def index():
		data = {
			"actions":			{},
			"data":				[],
		}

		action = request.args.get("action", None)
		if action != None:
			data["actions"][action] = request.args.get("param", None)
			
		return opsoroapp.render_template("assistant.html", **data)


		#subprocess.call("sudo python /home/pi/OnoSW/apps/opsoroassistant/IFTTT.py",shell=True)
	
	# @app_bp.route("/demo")
	# @opsoroapp.app_view
	# def demo():
	# 	data = {
	# 	}
	#
	# 	return opsoroapp.render_template("app.html", **data)

	# @app_bp.route("/play/<soundfile>", methods=["GET"])
	# @opsoroapp.app_api
	# def play(soundfile):
	# 	soundfiles = []
	# 	filenames = []

	# 	filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.wav"))

	# 	for filename in filenames:
	# 		soundfiles.append(os.path.split(filename)[1])

	# 	if soundfile in soundfiles:
	# 		Sound.play_file(soundfile)
	# 		return {"status": "success"}
	# 	else:
	# 		return {"status": "error", "message": "Unknown file."}

	# @app_bp.route("/saytts", methods=["GET"])
	# @opsoroapp.app_api
	# def saytts():
	# 	text = request.args.get("text", None)
	# 	if text is not None:
	# 		Sound.say_tts(text)
	# 	return {"status": "success"}


	@app_bp.route("/saytts", methods=["GET"])
	@opsoroapp.app_api
	def saytts():
	    subprocess.call("sudo halt", shell=True)
	    text = request.args.get("text", None)
	    if text is not None:
		    Sound.say_tts("Content Cursor Candidate")

	    return {"status": "successs"}
		

	@app_bp.route("/on", methods=["POST"])
	@opsoroapp.app_api
	def on():
		print("ON Selected")
		record()
		# if  __name__ == "__main__":
		# 	logging.basicConfig(filename='sound.log', format='%(filename)s [%(lineno)d] %(message)s',level=logging.INFO)

  #  		 #value = [];


		# def record():
  #  			while (True):

  #  			    start_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
		#         start_time = datetime.datetime.now()
		#         start = start_time.strftime('%Y-%m-%d %H:%M:%S')
		#         output_filename = 'rec.wav'

		    
		#         cmd = ['rec', '-c', '2', output_filename, 'rate', '8k', 'trim', '0', '10']
		#         call(cmd)

		#         os.rename("rec.wav", "/home/pi/OnoSW/data/assistant/rec.wav")

		#         end_time = datetime.datetime.now()
		#         end = end_time.strftime('%Y-%m-%d %H:%M:%S')
		#         logging.info("%s ~ %s (%f)" %(start, end,(end_time-start_time).total_seconds()))
		#         time.sleep(1)


		#         output = subprocess.check_output("sox /home/pi/OnoSW/data/assistant/rec.wav -n stat 2>&1 | grep 'RMS     amplitude:'",stderr= subprocess.STDOUT, shell=True)
		#         value = output.split('     ')[2]
		        
		#         value = float(value)
		#         value = value * 10000
		#         print(value)
		#         if(value < 100):
		#             print("stil")
		#             record()
		#             time.sleep(10)
		            
		            
		            
		            
		#         else:
		#             print("luid")
		#             record()
		#             time.sleep(10)
		            
		            
		#         time.sleep(5)

		# record()


	# @app_bp.route("/off", methods=["POST"])
	# @opsoroapp.app_api
	# def off():
	#     cmd = "sudo pkill -f __init__.py"
	    #output = call(cmd, shell=True)
	    #subprocess.call("sudo service opsoro stop", shell=True)
	    

	    
	    #subprocess.call("sudo sh /home/pi/OnoSW/restart_opsoro_service.sh", shell=True)
	   


	    

	    


	    #p = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
	    
	    #print(output)

	    # return line



	    #p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

	    



	opsoroapp.register_app_blueprint(app_bp)

def setup(opsoroapp):
	pass

def start(opsoroapp):
	# Start update thread
	# global app_t
	# app_t = StoppableThread(target=AppLoop)
	# app_t.start();
	pass

def stop(opsoroapp):
	# Stop update thread
	# global app_t
	# if app_t is not None:
	# 	app_t.stop()
	pass



def record():
    while (True):
    	#if cookie status=off > break, return


        sched= BlockingScheduler(timezone=utc)

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
        # print value
        if(value < 100):
            print("stil")
            def GetCalenderMessages():
			    payload={'subject':'CALENDER'}
			    head={'Connection':'close'}
			    r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload,headers=head)
			    r= str(r.text)
			    if r is 'null':
				    print("No Message")
			    if r != None:
				    message=r.split('|')[1]
				    Sound.say_tts(message)
				    print(message)
				    with open("/home/pi/OnoSW/apps/assistant/static/activities", "a") as myfile:
					    myfile.write("calender --> " + message + "\n")
				    record()
		   		

            def GetNewsMessages():
			    payload={'subject':'NEWS'}
			    r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload)
			    r= r.text
			    if r is 'null':
				    print("No Message")
			    if r != None:
				    message=r.split('|')[1]
				    Sound.say_tts(message)
				    print(message)
				    with open("/home/pi/OnoSW/apps/assistant/static/activities", "a") as myfile:
					    myfile.write("news --> " + message + "\n")
				    record()
				

            def GetWeatherMessages():
	            payload={'subject':'WEATHER'}
	            head={'Connection':'close'}
	            r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload, headers=head)
	            r= str(r.text)
	            if r is 'null':
				    print("No Message")
	            if r != None:
		            message=r.split('|')[1]
		            Sound.say_tts(message)
		            print(message)
		            record()

		    sched= BlockingScheduler(timezone=utc)
            sched.add_job(GetCalenderMessages,'interval',id="calendarmessage_job",seconds=3)
            sched.add_job(GetNewsMessages,'interval', id='newsmessage_job',seconds=10)
            sched.add_job(GetWeatherMessages,'cron',day_of_week='mon-sun',hour=10,minute=5)
            sched.start()
            time.sleep(10)


		            
        else:
            print("luid")
            def GetCalenderMessages():
			    payload={'subject':'CALENDER'}
			    r = requests.get('http://opsoroassistant.azurewebsites.net/api/assistant',params=payload)
			    r= str(r.text)
			    if r is 'null':
				    print("No Message")
			    if r != None:
				    message=r.split('|')[1]
				    print(message)
				    with open("/home/pi/OnoSW/apps/assistant/static/activities", "a") as myfile:
					    myfile.write("calender --> " + message + "\n")
				    record()


            sched=BlockingScheduler(timezone=utc)
            sched.add_job(GetCalenderMessages,'interval',id="calendarmessage_job",seconds=3)
            sched.start()	
            time.sleep(10)
            
        time.sleep(5)



def function():
	pass