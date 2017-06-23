from __future__ import with_statement

import glob
import os
from functools import partial

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug import secure_filename

from opsoro.robot import Robot
from opsoro.sound import Sound

config = {
    'full_name':            'Sounds',
    'author':               'OPSORO',
    'icon':                 'fa-volume-up',
    'color':                'blue',
    'difficulty':           3,
    'tags':                 ['sound', 'music', 'speech', 'TTS', 'recording'],
    'allowed_background':   False,
    'multi_user':           False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.MANUAL
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


def setup_pages(opsoroapp):
  sounds_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

  @sounds_bp.route('/')
  @opsoroapp.app_view
  def index():
    data = {'soundfiles': []}

    filenames = []

    filenames.extend(glob.glob(get_path('../../data/sounds/*.wav')))
    filenames.extend(glob.glob(get_path('../../data/sounds/*.mp3')))
    filenames.extend(glob.glob(get_path('../../data/sounds/*.ogg')))

    for filename in filenames:
      data['soundfiles'].append(os.path.split(filename)[1])

    return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

  @sounds_bp.route('/upload', methods=['POST'])
  @opsoroapp.app_view
  def upload():
    file = request.files['soundfile']
    if file:
      if file.filename.rsplit('.', 1)[1] in ['wav', 'mp3', 'ogg']:
        filename = secure_filename(file.filename)
        file.save(
            os.path.join(get_path('../../data/sounds/'), filename))
        flash('%s uploaded successfully.' % file.filename, 'success')
        return redirect(url_for('.index'))
      else:
        flash('This type of file is not allowed.', 'error')
        return redirect(url_for('.index'))
    else:
      flash('No file selected.', 'error')
      return redirect(url_for('.index'))

  opsoroapp.register_app_blueprint(sounds_bp)


def setup(opsoroapp):
  pass


def start(opsoroapp):
  pass


def stop(opsoroapp):
  pass
