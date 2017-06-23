# -*- coding: utf-8 -*-
from __future__ import with_statement

import glob
import math
import os
import shutil
import time
from exceptions import RuntimeError
from functools import partial
import threading
import yaml
from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug import secure_filename

import cmath
from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.sound import Sound
from opsoro.sound.tts import TTS

from opsoro.stoppable_thread import StoppableThread

from opsoro.users import Users

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


import tweepy
import re
import json
import time

config = {
    'full_name':            'Tweader',
    'icon':                 'fa-hashtag',
    'color':                'blue',
    'difficulty':           1,
    'tags':                 ['twitter', 'hashtag', 'sound', 'expressions'],
    'allowed_background':   False,
    'multi_user':           True,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

dof_positions = {}

autoRead = None # globals -> can be decalerd in called methodes
loop_T = None # loop var for Stoppable Thread
loop_PlayTweet = None # loop that plays playArray
autolooping = None
Emoticons = []
lang = 'en' #lang that needs to be played
tweetArrayToPlay = [] #tweet array that needs to be played
playing = False
newTweet = False

access_token = '141268248-yAGsPydKTDgkCcV0RZTPc5Ff7FGE41yk5AWF1dtN'
access_token_secret = 'UalduP04BS4X3ycgBJKn2QJymMhJUbNfQZlEiCZZezW6V'
consumer_key = 'U2PILejmAYpd20ImoqdTZp4Rm'
consumer_secret = 'nacB6eTgMR4cpZzckG7pTGpV3WKBXoyDhn3feU1R24kY2Kf0QF'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def send_action(action):
    Users.send_app_data(config['formatted_name'], action, {})

def send_data(action, data):
    #def send_app_data(self, appname, action, data={}): from Opsoro.Users
    Users.send_app_data(config['formatted_name'], action, data)


def setup_pages(opsoroapp):
    tweader_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @tweader_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {'actions': {}, 'emotions': [], 'sounds': []}
        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @tweader_bp.route('/', methods=['POST'])
    @opsoroapp.app_view
    def post():
        data = {'actions': {}, 'emotions': [], 'sounds': []} # Overbodig ...

        # Auguste code --- Te verbeteren a.d.h.v. post actions
        if request.form['action'] == 'startTweepy':
            stopTwitter()
            if request.form['data']:
                # HashTag input
                json_data = json.loads(request.form['data']) # Decoding strigified JSON
                social_id = []
                social_id.append(json_data['socialID'])

                # Auto Read
                global autoRead
                autoRead = json_data['autoRead']

                # Start Tweepy stream
                startTwitter(social_id)

        if request.form['action'] == 'stopTweepy':
            stopTwitter()

        if request.form['action'] == 'autoLoopTweepyNext':
            print_info('autoLoopTweepyNext')
            global autolooping
            autolooping = 1
            stopTwitter()

        if request.form['action'] == 'autoLoopTweepyStop':
            #global autolooping
            autolooping = 0
            send_action(request.form['action'])

        if request.form['action'] == 'playTweet':
            if request.form['data']:
                tweepyObj = json.loads(request.form['data'])
                playTweet(tweepyObj)
        if request.form['action'] == 'toggleAutoRead':
            autoRead = not autoRead
            print_info(autoRead)

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    opsoroapp.register_app_blueprint(tweader_bp)

def playTweet(tweepyDataModel):
    global playing
    global newTweet
    global loop_PlayTweet
    if not loop_PlayTweet == None:
        loop_PlayTweet.stop()
        print_info('zou ook moeten stoppen')
    global lang
    global tweetArrayToPlay
    playing = True
    lang = tweepyDataModel['text']['lang']
    tweetArrayToPlay = getPlayArray(tweepyDataModel)
    loop_PlayTweet = StoppableThread(target=asyncReadTweet) #start playing Tweet


#getting new tweet
class MyStreamListener(tweepy.StreamListener):
    global playing
    global newTweet
    def on_status(self, status):
        newTweet = True
        if(status == "stopIt"):
            return False
        dataToSend = processJson(status)
        if dataToSend['text']['filtered'] != None:
            send_data('dataFromTweepy', dataToSend)
        if autoRead == True:
            print_info(playing)
            if playing == False:
                playTweet(dataToSend)
                newTweet = False
    def on_error(slef, status_code):
        print_info("Tweepy error: " + status_code)


myStreamListener = MyStreamListener()
myStream = None

# Default functions for setting up, starting and stopping an app
def setup(opsoroapp):
    pass

def start(opsoroapp):
    pass

def stop(opsoroapp):
    stopTwitter()
    if loop_PlayTweet != None:
        loop_PlayTweet.stop()

def startTwitter(twitterWords):
    global myStream
    global myStreamListener
    myStream = tweepy.Stream(auth= api.auth, listener=myStreamListener)
    myStream.filter(track=twitterWords, async=True)


def stopTwitter():
    global myStream
    global myStreamListener
    if myStream != None:
        myStream.disconnect()
        myStream.running = False
        #myStream._thread
        #stream closes after one mor response from twitter
        #myStreamListener.on_status("stopIt")
        print_info("twitter stop")

#process tweepy json
def processJson(status):
    data = {
        "user": {
            "username": status._json["user"]["screen_name"],
            "profile_picture": status._json["user"]["profile_image_url_https"]
        },
        "text": {
            "original": status.text,
            "filtered": filterTweet(status.text),
            "lang": status.lang
        }
    }

    return data

def filterTweet(text):
    #alles in nieuw object aanmaken en steken
    encodedstattext = text.encode('utf-8')
    strTweet = str(encodedstattext)
    strTweet = strTweet.replace("RT", "Retweet", 1)
    strTweet = strTweet.replace("#", "")
    #voor emoticons te verwijderen
    strTweet = strTweet.decode('unicode_escape').encode('ascii', 'ignore')
    strTweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', strTweet, flags=re.MULTILINE) # re -> import re (regular expression)
    strTweet = languageCheck(strTweet, lang)
    return strTweet

def languageCheck(strTweet,lang):
    if lang == "en":
        return strTweet.replace("@","from ", 1)
    elif lang == "nl":
        return strTweet.replace("@","van ", 1)
    elif lang == "de":
        return strTweet.replace("@","von ", 1)
    elif lang == "fr":
        return strTweet.replace("@","de ", 1)
    else:
        return strTweet


def playTweetInLanguage(tweepyObj):
    print_info("play tweet in language")
    if not os.path.exists("/tmp/OpsoroTTS/"):
        os.makedirs("/tmp/OpsoroTTS/")

    full_path = os.path.join(get_path("/tmp/OpsoroTTS/"), "Tweet.wav")
    print_info(full_path)

    if(tweepyObj['text']['lang'] == 'und'):
        return

    TTS.create_espeak(tweepyObj['text']['filtered'], full_path, tweepyObj['text']['lang'], "f", "5", "150")
    Sound._play(full_path)


def playTweetInLanguage(text, lang):
    print_info("play tweet in language")
    if not os.path.exists("/tmp/OpsoroTTS/"):
        os.makedirs("/tmp/OpsoroTTS/")

    full_path = os.path.join(get_path("/tmp/OpsoroTTS/"), "Tweet.wav")
    print_info(full_path)

    TTS.create_espeak(text, full_path, lang, "f", "5", "150")
    Sound._play(full_path)


# Emoticon functions
def asyncReadTweet():
    time.sleep(0.05)
    global loop_PlayTweet
    global tweetArrayToPlay
    global lang
    global autolooping
    global playing
    while not loop_PlayTweet.stopped():
        for item in tweetArrayToPlay:
            if item[0] == 'txt':
                playTweetInLanguage(filterTweet(item[1]), lang)
                Sound.wait_for_sound()
            else:
                Expression.set_emotion_name(item[1], -1)
        loop_PlayTweet.stop()
        print_info(autolooping)
        if autolooping == 1:
            send_action("autoLoopTweepyNext")
        playing = False





#check if the post has an standard emoticon
def getPlayArray(status):
    output = []
    teller = -1
    previousWasText = False
    emoticonStr = status["text"]["original"]
    for text in emoticonStr:
        emotions = []
        winking = len(re.findall(u"[\U0001F609]", text))
        angry = len(re.findall(u"[\U0001F620]", text))
        happy_a = len(re.findall(u"[\U0000263A]", text))
        happy_b = len(re.findall(u"[\U0000263b]", text))
        happy_c = len(re.findall(u"[\U0001f642]", text))
        thinking = len(re.findall(u"[\U0001F914]", text))
        frowning = len(re.findall(u"[\U00002639]", text))
        nauseated = len(re.findall(u"[\U0001F922]", text))
        astonished = len(re.findall(u"[\U0001F632]", text))
        neutral = len(re.findall(u"[\U0001F610]", text))
        fearful = len(re.findall(u"[\U0001F628]", text))
        laughing = len(re.findall(u"[\U0001F603]", text))
        tired = len(re.findall(u"[\U0001F62B]", text))
        sad = len(re.findall(u"[\U0001f641]", text))

        if winking > 0:
            emotions.append("tong")
        if angry > 0:
            emotions.append("angry")
        if happy_a > 0 or happy_b > 0 or happy_c > 0:
            emotions.append("happy")
        if frowning > 0:
            emotions.append("tired")
        if nauseated > 0:
            emotions.append("disgusted")
        if astonished > 0:
            emotions.append("surprised")
        if neutral > 0:
            emotions.append("neutral")
        if fearful > 0:
            emotions.append("afraid")
        if laughing > 0:
            emotions.append("laughing")
        if tired > 0:
            emotions.append("sleep")
        if sad > 0:
            emotions.append("sad")

        if not emotions:
            #this is a text obj
            if not previousWasText:
                teller = teller + 1
                output.append([])
                output[teller].append("txt")
                output[teller].append(text)
            else:
                output[teller][1] += text

            previousWasText = True
        else:
            #this is an emoticon
            teller += 1
            output.append([])
            output[teller].append("emj")
            output[teller].append(emotions[0])
            previousWasText = False


    return output
