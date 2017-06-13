from __future__ import with_statement

import os
from functools import partial

#Eigen libs
import json
import urllib
import re
import threading
import json
import sys
import time
import telepot
from telepot.loop import MessageLoop

from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread
from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
# from opsoro.stoppable_thread import StoppableThread
from opsoro.sound import Sound
from opsoro.users import Users


try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def send_data(action, data):
    Users.send_app_data(config["formatted_name"], action, data)


def constrain(n, minn, maxn): return max(min(maxn, n), minn)

# from opsoro.expression import Expression

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

config = {
    'full_name':            'Telegram',
    'author':               'howest',
    'icon':                 'fa-commenting-o',
    'color':                'orange',
    'difficulty':           4,
    'tags':                 [''],
    'allowed_background':   False,
    'multi_user':           True,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

def setup_pages(opsoroapp):
    telegram_bp = Blueprint(
        config['formatted_name'],
        __name__,
        template_folder='templates',
        static_folder='static')

    @telegram_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {'expressions': {}}

        icons_static_folder = '../../server/static/images/emojione/'

        data['expressions'] = Expression.expressions

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)



    @telegram_bp.route('/getmessages', methods=['GET'])
    def getmessages():
        #print_info("hallo")
        filename = os.path.join(telegram_bp.static_folder, 'messages.json')

        with open(filename, 'r') as message_file:
                json_data = json.load(message_file)
        return jsonify(json_data)
        #return redirect("/")

    @telegram_bp.route('/signcontacts', methods=['POST'])
    def signcontacts():

        data = {'actions': {}}
        contacts = request.form['contacts']
        print_info(contacts)
        data['contacts'] = contacts
        json_data = json.dumps(data)

        writeFile('contacts.json', json_data)
        getcontacts()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)
        #return redirect("/")

    @telegram_bp.route('/getcontacts', methods=['GET'])
    def getcontacts():

        json_data = readFile('contacts.json')
        return jsonify(json_data)

    @telegram_bp.route('/signbans', methods=['POST'])
    def signbans():

        data = {'bans': {}}
        bans = request.form['bans']
        data['bans'] = bans
        json_data = json.dumps(data)

        writeFile('banlist.json', json_data)
        getbans()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)
        # return redirect("/")

    @telegram_bp.route('/getbans', methods=['GET'])
    def getbans():

        json_data = readFile('banlist.json')
        return jsonify(json_data)

    def writeFile(jsonFile, data):

        filename = os.path.join(telegram_bp.static_folder, jsonFile)
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(data))
        return;

    def readFile(jsonFile):

        if os.path.exists(os.path.join(telegram_bp.static_folder, jsonFile)):
            filename = os.path.join(telegram_bp.static_folder, jsonFile)
            with open(filename, 'r') as readfile:
                try:
                    json_data = json.load(readfile)
                except:
                    print_info("File is empty")
                    json_data = "{}"
            return json_data
        print_info("File doesn't exist")
        return '{}'


    opsoroapp.register_app_blueprint(telegram_bp)

data = {}
data['messages'] = []

def loop():
            def handle(msg,offset=None):
                if offset:
                    u = urllib.urlopen('https://api.telegram.org/bot371183808:AAH4HHCDqNkmCEavf5oxI-9wG27DNoY-m_E/getUpdates?offset={}'.format(offset))
                u = urllib.urlopen('https://api.telegram.org/bot371183808:AAH4HHCDqNkmCEavf5oxI-9wG27DNoY-m_E/getUpdates')
                z = json.load(u)
                u.close
                update_ids = []
                for result in z['result']:
                    text = result["message"]["text"]
                    firstname = result["message"]["from"]["first_name"]
                    update_id = result["update_id"]
                    print text
                    text = text.encode('unicode_escape')
                    update_ids.append(int(result["update_id"]))
                    maxid = max(update_ids);
                    #print(maxid);
                    data['messages'].append({
                    'first_name' : firstname,
                    'message' : text,
                    "update_id" : update_id,
                    "maxid" : maxid
                    })

                    send_data("messageIncomming", result)

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
