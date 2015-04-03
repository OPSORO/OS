from __future__ import print_function

import os
import subprocess

import RPi.GPIO as GPIO
from tpa2016 import TPA2016, TPA2016_AGC_OFF
from Adafruit_PWM_Servo_Driver import PWM

class Hardware:
	PIN_MOSFET = 22
	PIN_LED_ACTIVE = 17
	ADDR_TPA2016 = 0x58
	ADDR_PCA9685 = 0x40

	def __init__(self, hwversion = 1):
		#GPIO setup
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.PIN_MOSFET, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		GPIO.setup(self.PIN_LED_ACTIVE, GPIO.OUT)
		GPIO.output(self.PIN_LED_ACTIVE, GPIO.HIGH)

		#Audio setup
		self.tpa = TPA2016(addr=self.ADDR_TPA2016)
		self.tpa.enable_channel(r=True, l=True)
		self.tpa.set_gain(13)
		self.tpa.set_agc_compression(TPA2016_AGC_OFF)
		#os.system("amixer sset PCM,0 95%")
		subprocess.Popen("amixer sset PCM,0 95%", shell=True)

		#Servo PWM driver setup
		self.pwm = PWM(self.ADDR_PCA9685, debug=False)
		self.pwm.setPWMFreq(60.4) #Causes the prescaler to be set to 100, thus 1 bit = 4 microseconds pulse width
		self.pwm.setAllPWM(0, 375) # 375*4 = 1500 microsec

	def __del__(self):
		self.servo_power_off()
		GPIO.output(self.PIN_LED_ACTIVE, GPIO.LOW)
		GPIO.cleanup()

	def servo_power_on(self):
		GPIO.setup(self.PIN_MOSFET, GPIO.OUT)
		GPIO.output(self.PIN_MOSFET, GPIO.LOW)

	def servo_power_off(self):
		GPIO.setup(self.PIN_MOSFET, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def set_servo_us(self, channel, us):
		offTime = (us+2)//4 # Divide by 4 to find the off time. Integer division always rounds down, so +2 is used to get a rounded result.
		#print(offTime)
		self.pwm.setPWM(channel, 0, offTime);

	def set_all_servo_us(self, us):
		offTime = (us+2)//4 # Divide by 4 to find the off time. Integer division always rounds down, so +2 is used to get a rounded result.
		#print(offTime)
		self.pwm.setAllPWM(0, offTime);

	def say_tts(self, text):
		# TODO: fix for async
		#os.system("pico2wave -w /tmp/onoTTS.wav \"" + text + "\"")
		#os.system("aplay /tmp/onoTTS.wav")
		subprocess.Popen("pico2wave -w /tmp/onoTTS.wav \"%s\" ; aplay /tmp/onoTTS.wav" % text, shell=True)
