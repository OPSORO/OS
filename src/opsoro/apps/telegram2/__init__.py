from __future__ import with_statement

from functools import partial
import os
import glob
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from werkzeug import secure_filename

from opsoro.sound import Sound
from opsoro.robot import Robot
from opsoro.expression import Expression
from opsoro.stoppable_thread import StoppableThread
from opsoro.console_msg import *
#Eigen libs
import urllib
import re
import threading
import json
import sys
import time
import telepot
from telepot.loop import MessageLoop

config = {
    'full_name':            'Telegram2',
    'icon':                 'fa-volume-up',
    'color':                'blue',
    'difficulty':           3,
    'tags':                 ['sound', 'music', 'speech', 'TTS', 'recording'],
    'allowed_background':   False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.MANUAL
}
config['formatted_name'] =  config['full_name'].lower().replace(' ', '_')


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


def setup_pages(opsoroapp):
    telegram_bp = Blueprint(
        config['formatted_name'],
        __name__,
        template_folder='templates',
        static_folder='static')

    @telegram_bp.route('/',methods=['GET'])
    @opsoroapp.app_view
    def index():

        data = {
        'expressions': {}
        }

        icons_static_folder = '../../server/static/images/emojione/'

        data['expressions'] = Expression.expressions
        #getmessages()
        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)





    @telegram_bp.route('/getmessages', methods=['GET'])
    def getmessages():
        #print_info("hallo")
        filename = os.path.join(telegram_bp.static_folder, 'messages.json')

        with open(filename, 'r') as message_file:
                json_data = json.load(message_file)
        return jsonify(json_data)
        #return redirect("/")


    opsoroapp.register_app_blueprint(telegram_bp)


data = {}
data['messages'] = []

def loop():
            def handle(msg):
                u = urllib.urlopen('https://api.telegram.org/bot371183808:AAH4HHCDqNkmCEavf5oxI-9wG27DNoY-m_E/getUpdates')
                z = json.load(u)
                u.close
                for result in z['result']:
                    text = result["message"]["text"]
                    firstname = result["message"]["from"]["first_name"]
                    print text
                    text = text.encode('unicode_escape')

                    data['messages'].append({
                    'first_name' : firstname,
                    'message' : text
                    })

                    with open('src/opsoro/apps/telegram/static/messages.json','w') as outfile:
                        json.dump(data,outfile)

                    print data
                    #datamessages['message'] = text
                    #print(json_data)

                    if(text.startswith('\U')):
                        print('emoji first + text')
                        emo = text[5:]
                        print(emo)
                        Expression.set_emotion_unicode(emo)
                        #Sound.say_tts(text)

                    elif('\U' in text):
                        print('text + emoji')
                        print(text)
                        emojitext = text.split('\U')
                        print(emojitext)
                        text = emojitext[0]
                        emo = emojitext[1][3:]
                        print(emo)
                        Expression.set_emotion_unicode(emo)
                        #Sound.say_tts(text)

                    else:
                        textonly = text
                        Sound.say_tts(textonly)

            bot = telepot.Bot('371183808:AAH4HHCDqNkmCEavf5oxI-9wG27DNoY-m_E')
            MessageLoop(bot,handle).run_as_thread()

            '''
                print test
                test = test.encode('unicode_escape')

                if(test.startswith('\U')):
                    print('emoji first + text')
                    emo = test[5:]
                    print(emo)
                    Expression.set_emotion_unicode(emo)
                    #Sound.say_tts(text)

                elif('\U' in test):
                    print('text + emoji')
                    print(test)
                    emojitext = test.split('\U')
                    print(emojitext)
                    text = emojitext[0]
                    emo = emojitext[1][3:]
                    print(emo)
                    Expression.set_emotion_unicode(emo)
                    Sound.say_tts(text)

                else:
                    textonly = test
                    Sound.say_tts(textonly)
                '''


def setup(opsoroapp):
    pass


def start(opsoroapp):
    global loop_t
    #global MessageLoop
    loop_t = StoppableThread(target=loop)

def stop(opsoroapp):
    global loop_t
    loop_t.stop()
    #global MessageLoop
    #StoppableThread.stop(opsoroapp)
    print("stop")
