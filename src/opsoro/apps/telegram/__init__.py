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
from pprint import pprint
from opsoro.telepot import loop
from opsoro.telepot.loop import MessageLoop
from opsoro.telepot import *
from opsoro.telepot import Bot
from opsoro.apps.blacklist import scanSwearWordsInText
from opsoro.apps.blacklist import scanSwearWordsInText
from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread
from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
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

        data = {'contacts': {}}
        contacts = json.loads(request.form['contacts'])

        data['contacts'] = contacts

        writeFile('contacts.json', data)
        getcontacts()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)
        #return redirect("/")

    @telegram_bp.route('/getcontacts', methods=['GET'])
    def getcontacts():

        json_data = readFile('contacts.json')
        return jsonify(json.loads(json_data))

    @telegram_bp.route('/signbans', methods=['POST'])
    def signbans():

        data = {'bans': {}}
        bans = json.loads(request.form['bans'])
        data['bans'] = bans

        writeFile('banlist.json', data)
        getbans()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)
        # return redirect("/")

    @telegram_bp.route('/getbans', methods=['GET'])
    def getbans():

        json_data = readFile('banlist.json')
        return jsonify(json.loads(json_data))

    @telegram_bp.route('/signsettings', methods=['POST'])
    def signsettings():

        data = {'settings': {}}
        api = request.form
        data['settings'] = api

        writeFile('settinglist.json', data)
        getsettings()


        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)
        # return redirect("/")

    @telegram_bp.route('/getsettings', methods=['GET'])
    def getsettings():

        json_data = readFile('settinglist.json')
        return jsonify(json.loads(json_data))

    @telegram_bp.route('/getLastMessages', methods=['GET'])
    def getLastMessages():

        json_data = readFile('messages.json')
        return jsonify(json.loads(json_data))

    def writeFile(jsonFile, data):

        global mls
        mls.stop_threads()
        filename = os.path.join(telegram_bp.static_folder, jsonFile)
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(data))
        api_key  = getTelegramApiKey()
        loop(api_key)
        return;


    opsoroapp.register_app_blueprint(telegram_bp)

data = {}
data['messages'] = []
#mls = None

#functie voor te bepalen of het bericht een emoji bevat
def emojis(text,swearword):
     #dit kijkt of er daadwerkelijk een emoji in het bericht zit
    if('\U' in text):
         #begint de tekst met een emoji?
        if(text.startswith('\U')):
            print(text)
            #bij meerdere emojis worden deze ook gesplit
            emojitext = text.split('\\')
            print emojitext
            lengthemojitext = len(emojitext)
            print lengthemojitext
             #de verschillende emojis uitbeelden maar niet uitspreken
            for y in range(0,lengthemojitext):
                if('U0001' in emojitext[y]):
                    print('emoji')
                    print emojitext[y][4:]
                    Expression.set_emotion_unicode(emojitext[y][4:])
                    #tussen elke emoji 2seconden wachten
                    time.sleep(2)
                 #tekst wordt uitgesproken
                else:
                    print('text')
                    print(emojitext[y])
                    Sound.say_tts(emojitext[y])
                    print ('test')
 #de else wordt uitgevoerd wanneer het bericht start met een letter en een emoji bevat
        else:
            print('text + emoji')
            print(text)
            #de tekst en emoji van elkaar splitsen
            emojitext = text.split('\U')
            print(emojitext)
            lengthemojitext = len(emojitext)
            print lengthemojitext
            for y in range(0,lengthemojitext):
                print y
                 #de verschillende emojis uitbeelden maar niet uitspreken
                if('000' in emojitext[y]):
                    print('emoji')
                    print emojitext[y][3:]
                    Expression.set_emotion_unicode(emojitext[y][3:])
                     #tussen elke emoji 2 seconden wachten
                    time.sleep(2)
                #tekst wordt uitgesproken
                else:
                    print('text')
                    print emojitext[y]
                    Sound.say_tts(emojitext[y])
                    print ('test')
                    #time.sleep(5)
    #deze else wordt uitgevoerd wanneer het bericht enkel tekst bevat
    else:
        textonly = text
        Sound.say_tts(swearword)

def sendmessages(firstname,lastname,text,time,result,originaltext):
    #kijken of de gebruiker wel in de contactenlijst zit
    with open('src/opsoro/apps/telegram/static/contacts.json') as data_file:
        dict = json.load(data_file)
        lengte = len(dict["contacts"])

    for x in range(0, lengte):
        contactsName = dict["contacts"][x]["name"]
        lastnaamke = dict["contacts"][x]["lastname"]
        print dict["contacts"][x]
        if firstname in dict["contacts"][x].values() and lastname in dict["contacts"][x].values():

            data['messages'].insert(0,{
            'first_name' : firstname,
            'last_name' : lastname,
            'message' : text,
            'time' : time
            })
             #data versturen naar js
            send_data("messageIncomming", result)
            #berichten wegschrijven naar de messages.json
            with open('src/opsoro/apps/telegram/static/messages.json','w') as outfile:
                json.dump(data,outfile)

            emojis(originaltext,text)
         #als het bericht '/start' is, kijken of het een nieuwe gebruiker is
        elif(text == '/start'):
            print 'moet checken of toegelaten'
                #pass
             #doorsturen naar js
            send_data("messageIncomming", result)
        else:
            print 'gebruiker niet toegelaten'


def loop(api_key):

            localApiKey = ''
            if api_key != '':
                localApiKey = api_key
            else:
                localApiKey = getTelegramApiKey()
             #als de API key niet leeg is deze functie uitvoeren
            if localApiKey != '':
                 #de handle functie haalt onze berichten op
                def handle(msg):
                     #berichten worden opgehaald van deze link wat de dynamische API key bevat
                    u = urllib.urlopen('https://api.telegram.org/bot'+localApiKey+'/getUpdates')
                    z = json.load(u)
                    u.close
                    update_ids = []
                     #alle nodige informatie ophalen van de telegram link
                    for result in z['result']:
                        originaltext = result["message"]["text"]
                         #de emojis omzetten naar unicode
                        originaltext = originaltext.encode('unicode_escape')
                         #kijken of het bericht niet '/start' is, want dat wil zeggen dat het een nieuwe gebruiker is
                        if result["message"]["text"] != '/start':
                            result["message"]["text"] = scanSwearWordsInText(result["message"]["text"])
                        text = result["message"]["text"]
                        time = result["message"]["date"]
                        firstname = result["message"]["from"]["first_name"]
                        lastname = result["message"]["from"]["last_name"]
                        userid = result["message"]["from"]["id"]
                        print userid
                        update_id = result["update_id"]
                        text = text.encode('unicode_escape')
                        update_ids.append(int(result["update_id"]))
                        maxid = max(update_ids);

                        #de lijst met geblokkeerde personen ophalen
                        with open('src/opsoro/apps/telegram/static/banlist.json') as ban_file:
                            dictBan = json.load(ban_file)
                            lengteban = len(dictBan["bans"])
                         #wanneer er geen geblokkerde personen zijn deze functie uitvoeren
                        if lengteban == 0:
                            print 'Banlist is leeg ERROR'
                            sendmessages(firstname,lastname,text,time,result,originaltext)

                        else:
                            sendmessages(firstname,lastname,text,time,result,originaltext)



                #het bot api ophalen
                bot = Bot(localApiKey)
                global mls
                 # de MessageLoop is een functie uit de telepot library wat berichten ophaald
                mls = MessageLoop(bot,handle)
                 # als thread laten werken zodat hij blijft berichten ophalen
                mls.start_threads()

def readFile(jsonFile):

    telegram_bp = Blueprint(
        config['formatted_name'],
        __name__,
        template_folder='templates',
        static_folder='static')

    if os.path.exists(os.path.join(telegram_bp.static_folder, jsonFile)):
        filename = os.path.join(telegram_bp.static_folder, jsonFile)
        with open(filename, 'r') as readfile:
            try:
                json_data = json.load(readfile)
            except:
                print_info("File is empty")
                json_data = "{}"
        return json.dumps(json_data)
    print ("File doesn't exist")
    return '{}'


def getTelegramApiKey():

    API_KEY = ''
    settingsList = readFile('settinglist.json')
    if settingsList != '{}':
        settingsList = json.loads(settingsList)
        API_KEY = settingsList['settings']['apiKey']

    print(API_KEY)
    return API_KEY;

def setup(opsoroapp):
    pass


def start(opsoroapp):
     #API key ophalen bij de start
    api_key  = getTelegramApiKey()
    #de loop starten bij start
    loop(api_key)

def stop(opsoroapp):
    global mls

    #bij afsluiten van onze applicatie de MessageLoop thread stoppen
    mls.stop_threads()
