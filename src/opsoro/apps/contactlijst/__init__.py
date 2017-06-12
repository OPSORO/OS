from __future__ import with_statement

import glob
import math
import os
import shutil
import time
import json
from exceptions import RuntimeError
from functools import partial

import yaml
from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
from werkzeug import secure_filename

import cmath
from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def constrain(n, minn, maxn): return max(min(maxn, n), minn)

# from opsoro.expression import Expression


config = {
    'full_name':            'Contactlijst',
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


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

dof_positions = {}


def send_stopped():
    Users.send_app_data(config['formatted_name'], 'soundStopped', {})


def SocialscriptRun():
    Sound.wait_for_sound()
    send_stopped()


socialscript_t = None


def setup_pages(opsoroapp):
    contacts_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @contacts_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {'contacts': {}}

        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        getcontacts()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @contacts_bp.route('/signcontacts', methods=['POST'])
    def signcontacts():
        data = {'actions': {}}

        contacts = request.form['contacts']
        print_info(contacts)
        data['contacts'] = contacts
        json_data = json.dumps(data)


        filename = os.path.join(contacts_bp.static_folder, 'contacts.json')
        with open(filename, 'w') as contact_file:
                contact_file.write(json.dumps(json_data))

        getcontacts()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)
        #return redirect("/")

    @contacts_bp.route('/getcontacts', methods=['GET'])
    def getcontacts():

        filename = os.path.join(contacts_bp.static_folder, 'contacts.json')
        with open(filename, 'r') as contact_file:
                json_data = json.load(contact_file)
        return jsonify(json_data)

    opsoroapp.register_app_blueprint(contacts_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass