
import base64
import os
from functools import partial, wraps

import pluginbase
import yaml
from flask import Blueprint
from flask_login import LoginManager, current_user, login_user, logout_user
from sockjs.tornado import SockJSConnection

from opsoro.console_msg import *

from . import usertypes

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

try:
    import simplejson as json
    print_info('Using simplejson')
except ImportError:
    import json
    print_info('Simplejson not available, falling back on json')


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class _Users(object):
    def __init__(self):
        """
        Users class.
        """
        self.users = {}
        self.sockets = set()
        self.robot_sockets = set()
        self.sockjs_message_cb = {}
        self.last_robot_data = {}
        self.app_change_handler = None

    def setup(self, flaskapp):
        # Setup login manager
        self.login_manager = LoginManager()
        self.login_manager.init_app(flaskapp)
        self.login_manager.anonymous_user = usertypes.Guest
        self.login_manager.login_view = 'login'
        self.setup_loaders()

    def login_guest(self):
        usr = usertypes.Guest()
        login_user(usr, remember=False)
        self.users[usr.id] = usr

    def login_admin(self):
        usr = usertypes.Admin()
        login_user(usr, remember=False)
        self.users[usr.id] = usr

    def login_play(self):
        usr = usertypes.Play()
        login_user(usr, remember=False)
        self.users[usr.id] = usr

    def logout(self):
        # send message to all instances of the user
        self.broadcast_data('refresh', {}, current_user.sockets)
        # remove user from list

        if current_user.id in self.users:
            self.users.pop(current_user.id)
        # logout user
        logout_user()

    def logout_others(self):
        if current_user is None or not current_user.is_authenticated or not current_user.is_admin:
            return

        socks = set()

        tmp = set(self.users)
        for usr_id in tmp:
            if usr_id != current_user.id:
                usr = self.users.pop(usr_id)
                socks.update(usr.sockets)

        # send message to all other users
        self.broadcast_message('You have been logged out by an admin.', socks)

    def send_app_data(self, appname, action, data={}):
        for sock in self.sockets:
            if sock.activeapp == appname:
                data['action'] = action
                sock.send_data('app', {'data': data})
                return

    def broadcast_data(self, action, data={}, sockets=None):
        sender = None

        if sockets:
            sender = set(sockets)
        else:
            sender = set(self.sockets)

        if sender:
            sender.pop().broadcast_data(action, data, sockets)

    def broadcast_robot(self, data={}, save_last=False):
        if save_last:
            self.last_robot_data = data
        self.broadcast_data('robot', data, self.robot_sockets)

    def broadcast_message(self, message='', sockets=None):
        self.broadcast_data('info', {'type': 'popup', 'text': message}, sockets)

    def setup_loaders(self):
        @self.login_manager.user_loader
        def load_user(token):
            if token in self.users:
                return self.users.get(token)
            return

        @self.login_manager.unauthorized_handler
        def unauthorized_handler():
            print_error('Unauthorized')
            return 'Unauthorized'


Users = _Users()


class SocketConnection(SockJSConnection):
    """Socket connection implementation"""
    # Class level variable
    sockets = set()

    def __init__(self, *args, **kwargs):
        super(SocketConnection, self).__init__(*args, **kwargs)
        self._authenticated = False
        self.activeapp = None
        self._token = None
        self.robot = False

    def on_message(self, msg):
        # Attempt to decode JSON
        try:
            message = json.loads(msg)
        except ValueError:
            self.send_error('Invalid JSON')
            return

        action = message.pop('action', '')
        if action == 'robot':
            self.robot = True
            Users.sockets.remove(self)
            Users.robot_sockets.add(self)
            self.send_data('robot', Users.last_robot_data)

        if not self._authenticated:
            # Attempt to authenticate the socket
            try:
                if action == 'authenticate':
                    token = base64.b64decode(message['token'])
                    if token is not None and token in Users.users.keys():
                        usr = Users.users.get(token)
                        if usr is not None and usr.token == token and usr.token is not None:
                            # Auth succeeded
                            self._authenticated = True
                            self._token = token
                            self.activeapp = message.pop('app', None)
                            Users.app_change_handler()

                            usr.sockets.add(self)
                            return
                # Auth failed
                return
            except KeyError:
                # Auth failed
                return
        else:
            # Decode action and trigger callback, if it exists.
            if self.activeapp in Users.sockjs_message_cb:
                if action in Users.sockjs_message_cb[self.activeapp]:
                    Users.sockjs_message_cb[self.activeapp][action](self, message)

    def on_open(self, info):
        # Connect callback is triggered when socket is authenticated.
        Users.sockets.add(self)
        self.update_users()

    def on_close(self):
        if self._token is not None and self._token in Users.users:
            usr = Users.users.get(self._token)
            usr.sockets.discard(self)
        if self.activeapp:
            Users.app_change_handler()
        if self in Users.sockets:
            Users.sockets.remove(self)
        if self in Users.robot_sockets:
            Users.robot_sockets.remove(self)
        self.update_users()

    def send_error(self, message):
        return self.send(json.dumps({'action': 'error', 'status': 'error', 'message': message}))

    def send_data(self, action, data):
        msg = {'action': action, 'status': 'success'}
        msg.update(data)

        return self.send(json.dumps(msg))

    def broadcast_data(self, action, data, socks=None):
        msg = {'action': action, 'status': 'success'}
        msg.update(data)
        if socks is None:
            socks = Users.sockets
        return self.broadcast(socks, json.dumps(msg))

    def update_users(self):
        # Print current client count
        self.broadcast_data('users', {'count': (len(Users.users))})

    #
    #
    # def on_message(self, msg):
    #     # Attempt to decode JSON
    #     self.broadcast(self.client_sockets, msg)
    #     print msg
    #     pass
