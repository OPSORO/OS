from __future__ import with_statement

import json
import os
import time
# ------------------------------------------------------------------------------
# Facebook stuff ---------------------------------------------------------------
# ------------------------------------------------------------------------------
import urllib2
from functools import partial
from random import randint

# ------------------------------------------------------------------------------
# Twitter stuff ----------------------------------------------------------------
# ------------------------------------------------------------------------------
import tweepy
from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for)

from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

config = {
    'full_name':            'Social Response',
    'author':               'OPSORO',
    'icon':                 'fa-share-square',
    'color':                'blue',
    'difficulty':           3,
    'tags':                 ['social', 'facebook', 'twitter'],
    'allowed_background':   True,
    'multi_user':           False,
    'connection':           Robot.Connection.ONLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

loop_t = None
loop_button_t = None
# running = False


def get_page_data(page_id, fields, access_token):
    api_endpoint = "https://graph.facebook.com/v2.4/"
    fb_graph_url = api_endpoint + page_id + '?fields=' + fields + '&access_token=' + access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)

        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON error"

    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason


page_id = 'opsoro'  # username or id
field = 'fan_count'
token = 'EAAaBZCzjU8H8BAFV7KudJn0K1V12CDBHqTIxYu6pVh7cpZAbt1WbZCyZBeSZC472fpPd0ZAkWC1tMrfAY26XnQJUR2rNrMQncQ9OGJlie3dUeQVvabZCwNmGaLL4FGHjZBVTajid16FL5niGWytlwZCiFDgj6yjIsZAAAZD'  # Access Token

# Variables that contains the user credentials to access Twitter API
access_token = '735437381696905216-BboISY7Qcqd1noMDY61zN75CdGT0OSc'
access_token_secret = 'd3A8D1ttrCxYV76pBOB389YqoLB32LiE0RVyoFwuMKUMb'
consumer_key = 'AcdgqgujzF06JF6zWrfwFeUfF'
consumer_secret = 'ss0wVcBTFAT6nR6hXrqyyOcFOhpa2sNW4cIap9JOoepcch93ky'

twitterWords = ['#opsoro']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# override tweepy.StreamListener to add logic to on_status


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # print(status.text)
        # Go_Crazy(text=status.text, twitter=True)
        txt = status.text
        for tword in twitterWords:
            txt = txt.replace(tword, '')
        Go_Crazy(text=txt, twitter=True)


api = tweepy.API(auth)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# followers = []
# likes = 0
# counter = 0
sleep_time = 5

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Laughing Happy Sad Angry Surprised Afraid Disgusted Tired
emotions_phis = [36.0, 18.0, 198.0, 153.0, 90.0, 125.0, 172.0, 270.0]
sounds = ['smb_1-up.wav', 'smb_coin.wav', 'smb_powerup.wav', 'Whistle.wav', 'Woohoo.wav', 'Small_Applause.wav']
sound_int = -1
emotion_int = -1
prev_emotion_int = emotion_int
prev_sound_int = sound_int


def Go_Crazy(text='', twitter=False, facebook=False):
    print_info('Do something!')

    global prev_emotion_int
    global emotion_int
    global prev_sound_int
    global sound_int

    while sound_int == prev_sound_int:
        sound_int = randint(0, len(sounds) - 1)

    while emotion_int == prev_emotion_int:
        emotion_int = randint(0, len(emotions_phis) - 1)

    prev_sound_int = sound_int
    prev_emotion_int = emotion_int

    if len(text) > 1:
        Sound.say_tts(text)
    else:
        Sound.play_file(sounds[sound_int])
    Expression.set_emotion_r_phi(1.0, emotions_phis[emotion_int], True, 0.5)

    Hardware.Serial.send('anim\n')

    if twitter:
        Hardware.Serial.send('set\nset 000000000000000000247e24247e24\n')

    if facebook:
        Hardware.Serial.send('set\nset 00000000000000000818185f5f5f5e5e\n')

    loop_t.sleep(2)

    print_info('Done doing something!')


def LoopButton():
    time.sleep(0.05)  # delay
    while not loop_button_t.stopped():
        if Hardware.Analog.read_channel(0) > 1000:
            Go_Crazy()
            Sound.wait_for_sound()
        loop_button_t.sleep(0.02)


def Loop():
    time.sleep(0.05)  # delay
    counter = 0
    # Initialize current Likes
    # global likes
    likes = 0
    try:
        likes = int(get_page_data(page_id, field, token)[field])
    except Exception as e:
        pass

    # Initialize current followers
    # global followers
    followers = []
    new_followers = []
    for user in tweepy.Cursor(api.followers, screen_name=page_id).items():
        followers.append(user.name)

    while not loop_t.stopped():
        # if running:
        data = {}
        print_info('Checking social...')
        try:
            # Facebook:
            new_likes = int(get_page_data(page_id, field, token)[field])
            if new_likes > likes:
                print_info('Facebook: ' + str(new_likes - likes) + ' new likes.')
                Go_Crazy(facebook=True)

            likes = new_likes
            # print "Likes: "+ str(page_data[field])

            # Twitter requests: 1/minute
            if len(new_followers) > 0:
                username = new_followers.pop()
                followers.append(username)
                Go_Crazy(text='Hello ' + str(username), twitter=True)

            # global counter
            counter += 1
            if counter >= (60 / sleep_time):
                for user in tweepy.Cursor(api.followers, screen_name=page_id).items():
                    if user.name not in followers:
                        new_followers.append(user.name)
                        # print 'new follower: ', user.name
                if len(new_followers) > 0:
                    print_info('Twitter: ' + str(len(new_followers)) + ' new followers.')
                counter = 0

        except Exception as e:
            print e
            print_warning('Social error, internet, limit, ...?')

        loop_t.sleep(sleep_time)


def setup_pages(opsoroapp):
    app_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @app_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {
            'actions': {},
            'data': [],
        }

        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    global loop_t
    global loop_button_t
    global myStream
    myStream.filter(track=twitterWords, async=True)
    loop_t = StoppableThread(target=Loop)
    loop_button_t = StoppableThread(target=LoopButton)


def stop(opsoroapp):
    global loop_t
    global loop_button_t
    global myStream
    myStream.disconnect()
    loop_t.stop()
    loop_button_t.stop()
