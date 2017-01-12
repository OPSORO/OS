from flask import Blueprint, render_template

config = {'full_name': 'Circumplex',
          'icon': 'fa-meh-o',
          'color': '#15e678',
          'allowed_background': False,
          'robot_state': 1}

# robot_state:
# 0: Manual start/stop
# 1: Start robot automatically (alive feature according to preferences)
# 2: Start robot automatically and enable alive feature
# 3: Start robot automatically and disable alive feature


def setup_pages(opsoroapp):
    circumplex_bp = Blueprint(
        config['full_name'].lower(),
        __name__,
        template_folder='templates',
        static_folder='static')

    @circumplex_bp.route('/')
    @opsoroapp.app_view
    def index():
        data = {}
        return opsoroapp.render_template(config['full_name'].lower() + '.html',
                                         **data)

    opsoroapp.register_app_blueprint(circumplex_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
