from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.expression import Expression
from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread

import time

from functools import partial
import os

import json
import urllib2
from functools import partial
from random import randint

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

config = {
    'full_name':            'Facebook Live',
    'icon':                 'fa-video-camera',
    'color':                'red',
    'difficulty':           1,
    'tags':                 ['template', 'developer'],
    'allowed_background':   False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] =  config['full_name'].lower().replace(' ', '_')

def setup_pages(server):
    app_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')


    @app_bp.route('/')
    @server.app_view
    def index():
        data = {
            'actions': {},
            'data': [],
        }
        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        return server.render_template(config['formatted_name'] + '.html', **data)

    server.register_app_blueprint(app_bp)


def get_page_data(page_id, fields, access_token):
    api_endpoint = "https://graph.facebook.com/v2.8/"
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
token = 'EAAaBZCzjU8H8BAFV7KudJn0K1V12CDBHqTIxYu6pVh7cpZAbt1WbZCyZBeSZC472fpPd0ZAkWC1tMrfAY26XnQJUR2rNrMQncQ9OGJlie3dUeQVvabZCwNmGaLL4FGHjZBVTajid16FL5niGWytlwZCiFDgj6yjIsZAAAZD' # Access Token

loop_T = None

def loop():
    time.sleep(0.05)  # delay
    while not loop_T.stopped():

        data = get_page_data(page_id, field, token)
        print_info(data)
        loop_T.sleep(5)



# Default functions for setting up, starting and stopping an app
def setup(server):
    pass

def start(server):
    global loop_T
    loop_T = StoppableThread(target=loop)
    pass

def stop(server):
    loop_T.Stop();
    pass
