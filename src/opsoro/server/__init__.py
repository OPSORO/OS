import atexit
import base64
import logging
import os
import threading
from functools import partial, wraps

import pluginbase
import tornado.httpserver
import tornado.web
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_babel import Babel
from flask_login import current_user, logout_user
from sockjs.tornado import SockJSRouter
from tornado import web
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from opsoro.apps import Apps
from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.preferences import Preferences
from opsoro.robot import Robot
from opsoro.server.request_handlers import RHandler
from opsoro.users import SocketConnection, Users

# Helper function
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class Server(object):
  def __init__(self):
    self.request_handler = RHandler(self)

    # Create flask instance for webserver
    self.flaskapp = Flask(__name__)
    # self.flaskapp.config['DEBUG'] = True
    self.flaskapp.config['TEMPLATES_AUTO_RELOAD'] = True

    # Translation support
    self.flaskapp.config.from_pyfile('settings.cfg')
    self.babel = Babel(self.flaskapp)

    # Setup key for sessions
    self.flaskapp.secret_key = "5\x075y\xfe$\x1aV\x1c<A\xf4\xc1\xcfst0\xa49\x9e@\x0b\xb2\x17"

    # Setup login manager
    Users.setup(self.flaskapp)

    # Setup app system
    Apps.register_apps(self)
    # self.activeapp = None

    # Initialize all URLs
    self.request_handler.set_urls()

    # Run stop function at exit
    atexit.register(self.at_exit)

  def at_exit(self):
    print_info('Goodbye!')

    # Sleep robot
    Robot.sleep()

    Apps.stop_all()

    if threading.activeCount() > 0:
      threads = threading.enumerate()
      for thread in threads:
        try:
          thread.stop()
          thread.join()
        except AttributeError:
          pass

  def render_template(self, template, **kwargs):
    return self.request_handler.render_template(template, **kwargs)

  def run(self):
    # Setup SockJS

    flaskwsgi = WSGIContainer(self.flaskapp)

    self.socketrouter = SockJSRouter(SocketConnection, '/sockjs')

    tornado_app = tornado.web.Application(self.socketrouter.urls + [(r".*", tornado.web.FallbackHandler, {"fallback": flaskwsgi})])
    tornado_app.listen(80)

    # Wake up robot
    Robot.wake()

    # Start default app
    startup_app = Preferences.get('general', 'startup_app', None)
    if startup_app in Apps.apps:
      self.request_handler.page_openapp(startup_app)

    # SSL security
    # http_server = tornado.httpserver.HTTPServer(tornado_app, ssl_options={
    # 	"certfile": "/etc/ssl/certs/server.crt",
    # 	"keyfile": "/etc/ssl/private/server.key",
    # 	})
    # http_server.listen(443)

    try:
      # ioloop.PeriodicCallback(UserSocketConnection.dump_stats, 1000).start()
      IOLoop.instance().start()
    except KeyboardInterrupt:
      print_info('Keyboard interupt')
      self.at_exit()

  def shutdown(self):
    logging.info("Stopping server")
    io_loop = IOLoop.instance()
    io_loop.stop()

  def protected_view(self, f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      if current_user.is_authenticated:
        if current_user.is_admin:
          # the actual page
          return f(*args, **kwargs)
        else:
          flash("You do not have permission to access the requested page. Please log in below.")
          return redirect(url_for("login"))
      else:
        flash("You do not have permission to access the requested page. Please log in below.")
        return redirect(url_for("login"))

    return wrapper

  def app_view(self, f):
    appname = f.__module__.split(".")[-1]

    @wraps(f)
    def wrapper(*args, **kwargs):
      # Protected page
      if current_user.is_authenticated:
        if not current_user.is_admin:
          flash("You do not have permission to access the requested page. Please log in below.")
          return redirect(url_for("login"))
      else:
        flash("You do not have permission to access the requested page. Please log in below.")
        return redirect(url_for("login"))

      # Check if app is active
      if appname in Apps.active_apps:
        # This app is active
        return f(*args, **kwargs)
      else:
        # Return app not active page
        assert appname in Apps.apps, "Could not find %s in list of loaded apps." % appname
        data = {
            "app": {},
            # "appname": appname,
            "page_icon":    Apps.apps[appname].config["icon"],
            "page_caption": Apps.apps[appname].config["full_name"]
        }
        data["title"] = self.request_handler.title
        # if self.activeapp in Apps.apps:
        #     # Another app is active
        #     data["app"]["active"]   = True
        #     data["app"]["name"]     = Apps.apps[self.activeapp].config["full_name"]
        #     data["app"]["icon"]     = Apps.apps[self.activeapp].config["icon"]
        #     data["title"]           += " - %s" % Apps.apps[self.activeapp].config["full_name"]
        # else:
        #     # No app is active
        #     data["app"]["active"]   = False

        return render_template("app_not_active.html", **data)

    return wrapper

  def app_api(self, f):
    appname = f.__module__.split(".")[-1]

    @wraps(f)
    def wrapper(*args, **kwargs):
      # Protected page
      if current_user.is_authenticated:
        if not current_user.is_admin:
          return jsonify(status="error", message="You do not have permission to access the requested page.")
      else:
        return jsonify(status="error", message="You do not have permission to access the requested page.")

      # Check if app is active
      if appname in Apps.active_apps:
        # This app is active
        data = f(*args, **kwargs)
        if data is None:
          data = {}
        if "status" not in data:
          data["status"] = "success"

        return jsonify(data)
      else:
        # Return app not active page
        assert appname in Apps.apps, "Could not find %s in list of loaded apps." % appname

        return jsonify(status="error", message="This app is not active.")

    return wrapper
