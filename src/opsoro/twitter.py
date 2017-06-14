# -*- coding: utf-8 -*-
from __future__ import with_statement

import glob
import math
import os
import shutil
import time
from exceptions import RuntimeError
from functools import partial

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

def constrain(n, minn, maxn): return max(min(maxn, n), minn)

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))
#Global variables for the class to handle authorization
access_token = '735437381696905216-BboISY7Qcqd1noMDY61zN75CdGT0OSc'
access_token_secret = 'd3A8D1ttrCxYV76pBOB389YqoLB32LiE0RVyoFwuMKUMb'
consumer_key = 'AcdgqgujzF06JF6zWrfwFeUfF'
consumer_secret = 'ss0wVcBTFAT6nR6hXrqyyOcFOhpa2sNW4cIap9JOoepcch93ky'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

loop_T = None # loop var for wait_for_tweet
loop_E = None # loop var for Emoticons
Emoticons = []
hasRecievedTweet = False

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        dataToSend = Twitter.processJson(status)
        if dataToSend['text']['filtered'] != None:
            global hasRecievedTweet
            hasRecievedTweet = True
            Twitter.playEmotion(dataToSend)
            Twitter.playTweetInLanguage(dataToSend)

api = tweepy.API(auth)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

class _twitter(object):
    """docstring for _twitter."""
    def __init__(self):
        super(_twitter, self).__init__()
        #self.arg = arg

    def start_streamreader(self, hashtag):
        global hasRecievedTweet
        global myStream
        social_id = []
        social_id.append(hashtag)
        hasRecievedTweet = False #if adding ui elements to blockly this can be used to get out of a loop
        myStream.filter(track=social_id, async=True);
    def stop_streamreader(self):
        global myStream
        global hasRecievedTweet
        myStream.disconnect()
        hasRecievedTweet = False
        Sound.stop_sound()
    def get_tweet(self, hashtag):
        global loop_T
        self.start_streamreader(hashtag)
        loop_T = StoppableThread(target=self.wait_for_tweet)
    #streamreader stops after recieving a single tweet
    def wait_for_tweet(self):
        time.sleep(1)  # delay

        global loop_T
        while not loop_T.stopped():
            #stops the streamreader when it has recieved a single tweet
            global hasRecievedTweet
            if hasRecievedTweet == True:
                global myStream
                myStream.disconnect()
                print_info("stop twitter stream")
                loop_T.stop()
                pass
    #functions for filtering tweets
    def processJson(self, status):
        data = {
            "user": {
                "username": status._json["user"]["screen_name"],
                "profile_picture": status._json["user"]["profile_image_url_https"]
            },
            "text": {
                "original": status.text,
                "filtered": self.filterTweet(status),
                "lang": status.lang,
                "emoticon": self.checkForEmoji(status)
            }
        }
        return data
    def filterTweet(self, status):
        encodedstattext = status.text.encode('utf-8')
        strTweet = str(encodedstattext)
        strTweet = strTweet.replace("RT", "Retweet", 1)
        strTweet = strTweet.replace("#", "")
        strTweet = strTweet.decode('unicode_escape').encode('ascii', 'ignore')
        strTweet = strTweet.replace("https","")
        strTweet = strTweet.replace("http","")
        strTweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', strTweet, flags=re.MULTILINE) # re -> import re (regular expression)
        strTweet = self.languageCheck(strTweet, status)
        return strTweet
    def languageCheck(self, strTweet,status):
        if status.lang == "en":
            return strTweet.replace("@","from ", 1)
        elif status.lang == "nl":
            return strTweet.replace("@","van ", 1)
        elif status.lang == "de":
            return strTweet.replace("@","von ", 1)
        elif status.lang == "fr":
            return strTweet.replace("@","de ", 1)
        else:
            return strTweet
    #filter emoticons
    def checkForEmoji(self,status):
        emotions = []
        emoticonStr = status.text

        winking = len(re.findall(u"[\U0001F609]", emoticonStr))
        angry = len(re.findall(u"[\U0001F620]", emoticonStr))
        happy_a = len(re.findall(u"[\U0000263A]", emoticonStr))
        happy_b = len(re.findall(u"[\U0000263b]", emoticonStr))
        happy_c = len(re.findall(u"[\U0001f642]", emoticonStr))
        thinking = len(re.findall(u"[\U0001F914]", emoticonStr))
        frowning = len(re.findall(u"[\U00002639]", emoticonStr))
        nauseated = len(re.findall(u"[\U0001F922]", emoticonStr))
        astonished = len(re.findall(u"[\U0001F632]", emoticonStr))
        neutral = len(re.findall(u"[\U0001F610]", emoticonStr))
        fearful = len(re.findall(u"[\U0001F628]", emoticonStr))
        laughing = len(re.findall(u"[\U0001F603]", emoticonStr))
        tired = len(re.findall(u"[\U0001F62B]", emoticonStr))
        sad = len(re.findall(u"[\U0001f641]", emoticonStr))

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
            emotions.append("none")
        return emotions
    #functions to play emotions
    def playEmotion(self, tweet):
        global loop_E
        global Emoticons
        Emoticons = tweet['text']['emoticon']
        loop_E = StoppableThread(target=self.asyncEmotion)
    def asyncEmotion(self):
        time.sleep(0.05)

        global loop_E
        global Emoticons
        currentAnimationArrayLength = len(Emoticons)
        playedAnimations = 0
        while not loop_E.stopped():
            if currentAnimationArrayLength > playedAnimations:
                Expression.set_emotion_name(Emoticons[playedAnimations], -1)
                playedAnimations = playedAnimations+1
                time.sleep(2)
            if currentAnimationArrayLength == playedAnimations:
                loop_E.stop()
                pass
    #functions concerning sound
    def playTweetInLanguage(self, tweet):
        if not os.path.exists("/tmp/OpsoroTTS/"):
            os.makedirs("/tmp/OpsoroTTS/")

        full_path = os.path.join(
            get_path("/tmp/OpsoroTTS/"), "Tweet.wav")

        if os.path.isfile(full_path):
            os.remove(full_path)

        TTS.create_espeak(tweet['text']['filtered'], full_path, tweet['text']['lang'], "f", "5", "150")

        Sound.play_file(full_path)

# Global instance that can be accessed by apps and scripts
Twitter = _twitter()
