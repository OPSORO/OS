from __future__ import with_statement

import os
import json
from functools import partial

from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
# from opsoro.stoppable_thread import StoppableThread
from opsoro.sound import Sound


try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


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
    telegram_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @telegram_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {'actions': {}}

        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

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


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
