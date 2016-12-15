from __future__ import with_statement

from flask import Flask, request, send_from_directory

from opsoro.robot import Robot
from opsoro.hardware import Hardware
from opsoro.expression import Expression
from opsoro.sound import Sound
from opsoro.console_msg import *

import glob
import os
from functools import wraps, partial
# from werkzeug import secure_filename
get_abs_path = partial(os.path.join,
                       os.path.abspath(os.path.dirname(__file__)))

try:
    import simplejson as json
except ImportError:
    import json

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

# ------------------------------------------------------------------------------
# DOCUMENTS
# ------------------------------------------------------------------------------

docs_data_path = '../../data/'


def is_safe_path(path):
    if path is None:
        return False
    if path.find('..') >= 0:
        return False

    return True


def docs_file_data(app_name=None):
    file_name_ext = None

    file_name_ext = request.args.get('f', type=str, default=None)

    # if action == 'get':

    if not is_safe_path(file_name_ext):
        return json.dumps({'success': False,
                           'message': 'Provided data error.'})

    file_name_ext.replace('%2F', '/')

    defaultPath = docs_data_path
    if app_name is not None:
        defaultPath += app_name.lower()
    folderPath = get_abs_path(defaultPath + '/')

    if os.path.isfile(folderPath + file_name_ext):
        return send_from_directory(folderPath, file_name_ext)
    return json.dumps({'success': False, 'message': 'File error.'})


def docs_file_save(app_name):
    file_name = request.form.get('file_name', type=str, default=None)
    file_ext = request.form.get('file_extension', type=str, default=None)
    file_data = request.form.get('file_data', type=str, default=None)

    if file_data is None:
        return json.dumps({'success': False,
                           'message': 'Provided data error.'})

    if not is_safe_path(file_name) or not is_safe_path(file_ext):
        return json.dumps({'success': False,
                           'message': 'Provided data error.'})

    defaultPath = docs_data_path
    if app_name is not None:
        defaultPath += app_name.lower()

    folderPath = get_abs_path(defaultPath + '/')

    file_name_ext = (file_name + file_ext)

    with open(folderPath + file_name_ext, 'w') as f:
        f.write(file_data)

    return json.dumps({'success': True})


def docs_file_delete(app_name):
    file_name_ext = request.form.get('file_name_ext', type=str, default=None)

    if not is_safe_path(file_name_ext):
        return json.dumps({'success': False,
                           'message': 'Provided data error.'})

    defaultPath = docs_data_path
    if app_name is not None:
        defaultPath += app_name.lower()

    deleted = False

    file_name_ext = os.path.join(get_abs_path(defaultPath), file_name_ext)

    if os.path.isdir(file_name_ext):
        shutil.rmtree(file_name_ext)
        deleted = True

    if os.path.isfile(file_name_ext):
        os.remove(file_name_ext)
        deleted = True

    if not deleted:
        return json.dumps({'success': False,
                           'message': 'File could not be removed.'})

    return json.dumps({'success': True})


def docs_file_list():
    defaultPath = docs_data_path
    folderPath = defaultPath + '/'
    appSpecificFolderPath = ''
    get_ext = '.*'
    get_save = 0
    get_folders = 0

    # { a: app.name, p: currentpath, e: extension, f: onlyFolders, s: saveFileView }
    get_app_name = request.args.get('a', type=str, default=None)
    get_path = request.args.get('p', type=str, default=None)
    get_ext = request.args.get('e', type=str, default='.*')
    get_folders = request.args.get('f', type=int, default=0)
    get_save = request.args.get('s', type=int, default=0)

    if is_safe_path(get_app_name):
        defaultPath += get_app_name.lower().replace(' ', '_')
    folderPath = defaultPath + '/'

    # Make sure the file operations stay within the data folder
    if is_safe_path(get_path):
        if len(get_path) > 1 and get_path[-1] == '.':
            get_path = get_path[0:-1]

        # Make sure the file operations stay within the data folder
        if not is_safe_path(get_ext):
            get_ext = ''
    else:
        get_path = ''

    data = {'path': get_path, 'folders': [], 'files': []}

    if get_path != '':
        data['previouspath'] = get_path[0:get_path.rfind('/', 0, len(get_path)
                                                         - 1)] + '/'
        if get_path.rfind('/', 0, len(get_path) - 1) < 0:
            data['previouspath'] = '/'

    get_path = (folderPath + get_path)

    foldernames = glob.glob(get_abs_path(get_path + '*'))
    for foldername in foldernames:
        if ('.' not in os.path.split(foldername)[1]):
            data['folders'].append(os.path.split(foldername)[1] + '/')
    data['folders'].sort()

    if get_save == 1:
        data['savefileview'] = get_save

    if get_folders != 1:
        filenames = glob.glob(get_abs_path(get_path + '*' + get_ext))
        for filename in filenames:
            if '.' in os.path.split(filename)[1]:
                data['files'].append(os.path.split(filename)[1])
        data['files'].sort()
    else:
        data['onlyfolders'] = get_folders

    return data


# ------------------------------------------------------------------------------
# ROBOT
# ------------------------------------------------------------------------------
def robot_config_data():
    config_data = request.form.get('config_data', type=str, default=None)

    # This function also handles the None value and returns the current configuration
    tempConfig = Robot.config(config_data)

    if config_data is not None:
        Robot.save_config()

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
        Robot.set_dof_values(dof_values)

    tempDofs = Robot.get_dof_values()
    return json.dumps({'success': True, 'dofs': tempDofs})


def robot_tts():
    text = request.args.get('t', None)
    if is_safe_path(text):
        Sound.say_tts(text)

    return json.dumps({'success': True})


def robot_sound():
    soundfile = request.args.get('s', type=str, default=None)

    if not is_safe_path(soundfile):
        return json.dumps({'success': False, 'message': 'Unknown file.'})

    soundfiles = []
    filenames = []

    filenames = glob.glob(get_abs_path(docs_data_path + 'sounds/*.wav'))

    for filename in filenames:
        soundfiles.append(os.path.split(filename)[1])

    if soundfile in soundfiles:
        Sound.play_file(soundfile)

        return json.dumps({'success': True})
    else:
        return json.dumps({'success': False, 'message': 'Unknown file.'})


def robot_servo():
    servo_pin = request.form.get('pin_number', type=int, default=0)
    servo_value = request.form.get('value', type=int, default=1500)

    servo_pin = constrain(servo_pin, 0, 32)
    servo_value = constrain(servo_value, 500, 2500)

    # print_info('pin: ' + str(servo_pin) + ', value: ' + str(servo_value))

    with Hardware.lock:
        Hardware.servo_enable()
        Hardware.servo_set(servo_pin, servo_value)

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
        Hardware.servo_enable()
        Hardware.servo_set_all(values)

    return json.dumps({'success': True})


def robot_stop():
    Sound.stop_sound()
    return json.dumps({'success': True})
