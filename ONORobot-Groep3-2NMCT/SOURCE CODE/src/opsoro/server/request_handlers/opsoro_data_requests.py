from __future__ import with_statement

import glob
import os
from functools import partial

import yaml
from flask import request, send_from_directory

from opsoro.console_msg import *
from opsoro.data import Data
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.sound import Sound

get_abs_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

try:
    import simplejson as json
except ImportError:
    import json

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def constrain(n, minn, maxn): return max(min(maxn, n), minn)

# ------------------------------------------------------------------------------
# DOCUMENTS
# ------------------------------------------------------------------------------


def docs_file_data(app_name=None):
    file_name_ext = request.args.get('f', type=str, default=None)

    data = Data.read(app_name, file_name_ext)
    if data:
        return data

    return json.dumps({'success': False, 'message': 'File error.'})


def docs_file_save(app_name):
    file_name_ext = request.form.get('filename', type=str, default=None)
    file_data = request.form.get('data', type=str, default=None)

    if Data.write(app_name, file_name_ext, file_data):
        return json.dumps({'success': True})

    return json.dumps({'success': False, 'message': 'Provided data error.'})


def docs_file_delete(app_name):
    file_name_ext = request.form.get('filename', type=str, default=None)

    if Data.delete(app_name, file_name_ext):
        return json.dumps({'success': True})

    return json.dumps({'success': False, 'message': 'File could not be removed.'})


def docs_file_list():
    # { a: app.name, p: currentpath, e: extension, f: onlyFolders, s: saveFileView }
    get_app_name = request.args.get('a', type=str, default=None)
    get_ext = request.args.get('e', type=str, default='.*')
    get_save = request.args.get('s', type=int, default=0)

    data = {}

    data['files'] = Data.filelist(get_app_name, get_ext)

    if get_save == 1:
        data['savefileview'] = get_save

    return data


# ------------------------------------------------------------------------------
# ROBOT
# ------------------------------------------------------------------------------
def config_robot_data():
    config_data = request.form.get('config_data', type=str, default=None)

    # This function also handles the None value and returns the current configuration
    tempConfig = Robot.set_config(config_data)

    return json.dumps({'success': True, 'config': tempConfig})


def config_expressions_data():
    config_data = request.form.get('config_data', type=str, default=None)

    # This function also handles the None value and returns the current configuration
    tempConfig = Expression.set_config(config_data)

    return json.dumps({'success': True, 'config': tempConfig})


def robot_emotion():
    r = request.form.get('r', type=float, default=0.0)
    phi = request.form.get('phi', type=float, default=0.0)
    time = request.form.get('time', type=float, default=-1)

    # Set emotion with time (-1 for smooth animation based on distance of previous dof values)
    Expression.set_emotion_r_phi(r, phi, True, time)

    return json.dumps({'success': True})


def robot_dof_data():
    module_name = request.form.get('module_name', type=str, default='')
    dof_name = request.form.get('dof_name', type=str, default='')
    dof_value = request.form.get('value', type=float, default=0.0)

    dof_value = constrain(dof_value, -1.0, 1.0)

    Robot.set_dof_value(module_name, dof_name, dof_value)

    return json.dumps({'success': True})


def robot_dofs_data():
    dof_values = request.form.get('dofdata', type=str, default=None)

    # dof_values = request.form.get('values', type=str, default='')
    # print(dof_values)
    if dof_values is not None:
        dof_values = yaml.load(dof_values, Loader=Loader)
        if type(dof_values) is dict:
            Robot.set_dof_values(dof_values)
        elif type(dof_values) is list:
            Robot.set_dof_list(dof_values)

    tempDofs = Robot.get_dof_values()
    return json.dumps({'success': True, 'dofs': tempDofs})


def robot_tts():
    text = request.args.get('t', None)

    Sound.say_tts(text)

    return json.dumps({'success': True})


def robot_sound():
    soundfile = request.args.get('s', type=str, default=None)

    if Sound.play_file(soundfile):
        return json.dumps({'success': True})

    return json.dumps({'success': False, 'message': 'Unknown file.'})


def robot_servo():
    servo_pin = request.form.get('pin_number', type=int, default=0)
    servo_value = request.form.get('value', type=int, default=1500)

    servo_pin = constrain(servo_pin, 0, 32)
    servo_value = constrain(servo_value, 500, 2500)

    # print_info('pin: ' + str(servo_pin) + ', value: ' + str(servo_value))

    with Hardware.lock:
        Hardware.Servo.enable()
        Hardware.Servo.set(servo_pin, servo_value)

    return json.dumps({'success': True})


def robot_servos():
    servo_data = request.form.get('servo_data', type=int, default=None)

    values = []

    for value in servo_data:
        if value < 0:
            values.append(None)
        else:
            values.append(constrain(value, 500, 2500))

    with Hardware.lock:
        Hardware.Servo.enable()
        Hardware.Servo.set_all(values)

    return json.dumps({'success': True})


def robot_stop():
    Sound.stop_sound()
    return json.dumps({'success': True})
