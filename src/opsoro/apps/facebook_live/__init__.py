from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.expression import Expression
from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread
from opsoro.users import Users

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
    'difficulty':           3,
    'tags':                 ['template', 'developer'],
    'allowed_background':   False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] =  config['full_name'].lower().replace(' ', '_')


access_token = 'EAAEGfayCJKUBAAxLeDshftcnHfpm8tumGF9GWmkYVyRFUfVAYs5zVZAuUWjBHC6HsPzGCcj8wAV0aNo0WvYSbb5BFrHZCHlYrKcStcgAwSUcWyr5eAj6jh3vPZAMFtegRGkTCZC7NUZCXCZBv84rpxQ2qgoZCbA5ZBmfy8z9ox6FADLoCFZAtnismGY8kFd9Vk8MZD'  # Access Token

video_id = None
thread_fb_t = None
secOphalenData = 2

def thread_fb():
    time.sleep(0.05)  # delay

    global video_id
    global thread_fb_t

    while not thread_fb_t.stopped():
        getLiveVideoData(video_id)
        time.sleep(secOphalenData)
        pass

def send_data(action, data):
    Users.send_app_data(config['formatted_name'], action, data)


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


    @app_bp.route('/', methods=['POST'])
    @server.app_view
    def post():
        data = {'actions': {}, 'emotions': [], 'sounds': []}

        if request.form['action'] == 'getLiveVideos':
            fields = "live_videos"
            graph_response = get_graph_data("me", fields, access_token)
            if graph_response:
                send_data(request.form['action'], graph_response)

        if request.form['action'] == 'liveVideoIDs':
            if request.form['data']:
                global video_id
                global thread_fb_t
                video_id = json.loads(request.form['data'])[0]
                thread_fb_t = StoppableThread(target=thread_fb)
        if request.form['action'] == 'stopStream':
            #global thread_fb_t
            thread_fb_t.stop()

        return server.render_template(config['formatted_name'] + '.html', **data)

    server.register_app_blueprint(app_bp)

def getLiveVideoData(facebook_id):
    fields = "id,live_views,comments,status,stream_url,secure_stream_url,embed_html"
    graph_response = get_graph_data(facebook_id, fields, access_token)
    #print_info(graph_response)
    if graph_response:
        print_info(graph_response)
        send_data('liveVideoStats', graph_response)


def get_graph_data(facebook_id, fields, access_token):
    api_endpoint = "https://graph.facebook.com/v2.8/"
    fb_graph_url = api_endpoint + facebook_id + '?fields=' + fields + '&access_token=' + access_token

    print_info(fb_graph_url)

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


# Default functions for setting up, starting and stopping an app
def setup(server):
    pass

def start(server):
    pass

def stop(server):
    thread_fb_t.stop()
    pass
