from flask import Blueprint, render_template

from opsoro.robot import Robot

config = {
    'full_name':            'Circumplex',
    'author':               'OPSORO',
    'icon':                 'fa-circle-o-notch',
    'color':                'green',
    'difficulty':           0,
    'tags':                 ['circumplex', 'circle', 'expression'],
    'allowed_background':   False,
    'multi_user':           True,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')


def setup_pages(opsoroapp):
    circumplex_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @circumplex_bp.route('/')
    @opsoroapp.app_view
    def index():
        data = {}
        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    opsoroapp.register_app_blueprint(circumplex_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
