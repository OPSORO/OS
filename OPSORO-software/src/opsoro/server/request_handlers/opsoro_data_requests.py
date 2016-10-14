from flask import Flask, request, send_from_directory

from opsoro.robot import Robot
from opsoro.hardware import Hardware
from opsoro.expression import Expression

from opsoro.console_msg import *

import glob
import os
from functools import wraps, partial
get_abs_path = partial(os.path.join,
                       os.path.abspath(os.path.dirname(__file__)))

try:
    import simplejson as json
    print_info('Using simplejson')
except ImportError:
    import json
    print_info('Simplejson not available, falling back on json')

# ------------------------------------------------------------------------------
# DOCUMENTS
# ------------------------------------------------------------------------------

docs_data_path = '../../data/'


def docs_file_data(app_name=None):
    file_name_ext = None

    file_name_ext = request.args.get('f', type=str, default=None)

    # if action == 'get':

    if file_name_ext == None:
        return json.dumps({'success': False}), 200, {'ContentType':
                                                     'application/json'}
    file_name_ext.replace('%2F', '/')

    defaultPath = docs_data_path
    if app_name is not None:
        defaultPath += app_name.lower()
    folderPath = get_abs_path(defaultPath + '/')

    if os.path.isfile(folderPath + file_name_ext):
        return send_from_directory(folderPath, file_name_ext)
    return json.dumps({'success':
                       False}), 200, {'ContentType': 'application/json'}

    # return json.dumps({'success': True})


def docs_file_save(app_name):
    # if action == 'save':
    # if givenPath == None:
    #     return json.dumps({'success': False}), 200, {'ContentType':
    #                                                  'application/json'}

    defaultPath = docs_data_path
    if app_name is not None:
        defaultPath += app_name.lower()
    folderPath = get_abs_path(defaultPath + '/')

    file_name = request.form.get('filename', type=str, default=None)
    file_ext = request.form.get('fileextension', type=str, default=None)
    file_data = request.form.get('filedata', type=str, default='')

    file_name_ext = file_name + file_ext

    # if overwrite == 0:
    #     if os.path.isfile(folderPath + file_name_ext):
    #         return json.dumps({'success': False}), 200, {'ContentType':
    #                                                      'application/json'}
    # print_info(folderPath)
    # print_info(file_name_ext)

    with open(folderPath + file_name_ext, 'w') as f:
        f.write(file_data)

    return json.dumps({'success': True}), 200, {'ContentType':
                                                'application/json'}

    # return json.dumps({'success': True})


def docs_file_delete(app_name):
    # if action == 'delete':
    if givenPath == None:
        return json.dumps({'success': False}), 200, {'ContentType':
                                                     'application/json'}

    deleted = False

    if os.path.isdir(givenPath):
        shutil.rmtree(givenPath)
        deleted = True

    if os.path.isfile(givenPath):
        os.remove(os.path.join(get_abs_path(''), givenPath))
        deleted = True

    if deleted:
        return json.dumps({'success': True}), 200, {'ContentType':
                                                    'application/json'}
    else:
        return json.dumps({'success': False}), 200, {'ContentType':
                                                     'application/json'}

    return json.dumps({'success': True})


def docs_file_list():
    #
    # if self.server.activeapp != appname:
    #     return redirect('/openapp/%s' % appname)
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

    # if request.method == 'GET':
    if get_app_name is not None:
        defaultPath += get_app_name.lower().replace(' ', '_')
    folderPath = defaultPath + '/'

    # Make sure the file operations stay within the data folder
    if get_path is not None and get_path.find('..') >= 0:
        get_path = None
    if get_path is not None:
        if len(get_path) > 1 and get_path[-1] == '.':
            get_path = get_path[0:-1]

        # Make sure the file operations stay within the data folder
        if get_ext.find('..') >= 0:
            get_ext = ''
        # Append extension
        # if get_path[-len(get_ext):] != get_ext:
        #     get_path = get_path + get_ext

        # print_info('Files: ' + action + ': ' + get_abs_path(folderPath) +
        #            get_path)

    else:
        get_path = ''

    data = {'path': get_path, 'folders': [], 'files': []}

    # if action == 'newfolder':
    #     if get_path == None:
    #         return json.dumps(
    #             {'success': False}), 200, {'ContentType':
    #                                        'application/json'}
    #
    #     get_path = get_abs_path(get_path)
    #     if not os.path.exists(get_path):
    #         os.makedirs(get_path)
    #     else:
    #         return json.dumps(
    #             {'success': False}), 200, {'ContentType':
    #                                        'application/json'}
    #
    #     return json.dumps({'success': True}), 200, {'ContentType':
    #                                                 'application/json'}

    # Security check, should stay within data folder
    # if appSpecificFolderPath.find('..') >= 0:
    #     appSpecificFolderPath = ''
    #
    # while len(appSpecificFolderPath) > 0 and appSpecificFolderPath[0] == '/':
    #     appSpecificFolderPath = appSpecificFolderPath[1:]
    #
    # folderPath = folderPath + appSpecificFolderPath
    #
    # if len(appSpecificFolderPath) > 0 and appSpecificFolderPath[-1] != '/':
    #     appSpecificFolderPath = appSpecificFolderPath + '/'
    #
    # if folderPath[-1] != '/':
    #     folderPath = folderPath + '/'
    #
    # data = {'path': appSpecificFolderPath, 'folders': [], 'files': []}
    # # Only add a previous path if it is not in the base folder
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
    config_data = request.form.get('data', type=str, default='')

    return json.dumps({'success': True})


def robot_emotion():

    return json.dumps({'success': True})


def robot_dofs_data():
    tempDofs = Robot.get_dof_values()
    return json.dumps({'success': True, 'dofs': tempDofs})


def robot_tts():

    return json.dumps({'success': True})


def robot_sound():

    return json.dumps({'success': True})


def robot_servo():

    return json.dumps({'success': True})
