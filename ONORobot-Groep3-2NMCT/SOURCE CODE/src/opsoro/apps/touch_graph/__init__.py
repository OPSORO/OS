from __future__ import division, with_statement

import random
import threading
import time

from flask import Blueprint, flash, redirect, render_template, request, url_for

from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.stoppable_thread import StoppableThread

config = {
    'full_name':            'Touch Graph',
    'author':               'OPSORO',
    'icon':                 'fa-hand-o-down',
    'color':                'gray_light',
    'difficulty':           3,
    'tags':                 ['capacitive', 'touch', 'button'],
    'allowed_background':   False,
    'multi_user':           False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.MANUAL
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')


touch_t = None
running = False
numelectrodes = 0


def TouchLoop():
    time.sleep(0.05)  # delay

    global running

    while not touch_t.stopped():
        if running:
            data = {}

            with Hardware.lock:
                ret = Hardware.Capacitive.get_filtered_data()

            for i in range(numelectrodes):
                data[i] = ret[i]

            Users.send_app_data(config['formatted_name'], 'updateelectrodes', {'electrodedata': data})

        touch_t.sleep(0.1)


def startcap(electrodes):
    global running
    global numelectrodes

    Hardware.Capacitive.init(electrodes=electrodes, gpios=0, autoconfig=True)
    numelectrodes = electrodes

    running = True


def stopcap():
    global running
    running = False


def setup_pages(opsoroapp):
    touch_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @touch_bp.route('/')
    @opsoroapp.app_view
    def index():
        data = {}

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @opsoroapp.app_socket_message('startcapture')
    def s_startcapture(conn, data):
        electrodes = int(data.pop('electrodes', 0))
        startcap(electrodes)

    @opsoroapp.app_socket_message('stopcapture')
    def s_stopcapture(conn, data):
        stopcap()

    opsoroapp.register_app_blueprint(touch_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    global touch_t

    touch_t = StoppableThread(target=TouchLoop)
    # touch_t.start()


def stop(opsoroapp):
    global touch_t
    global running

    running = False
    touch_t.stop()
