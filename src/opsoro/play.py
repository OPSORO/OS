import urllib

import requests

from opsoro.console_msg import *

# PLAY_URL = 'https://robot.opsoro.be/'
PLAY_URL = 'https://opsoro.be/'


class _Play(object):
    def __init__(self):
        self.uuid = None
        self.token = None
        self.username = None
        self.password = None
        pass

    def is_online(self):
        try:
            data = urllib.urlopen(PLAY_URL)
            return True
        except Exception as e:
            return False

    def login(self, username=None, password=None):
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password

        if not self.is_online():
            return False

        url_login = PLAY_URL + 'accounts/login/'
        url_run = PLAY_URL + 'robot/token/'

        # # Use 'with' to ensure the session context is closed after use.
        with requests.Session() as s:
            s.get(url_login)
            csrftoken = s.cookies['csrftoken']
            payload = {
                'username': self.username,
                'password': self.password,
                'csrfmiddlewaretoken': csrftoken,
                'next': url_run
            }
            p = s.post(url_login, data=payload, headers=dict(Referer=url_login))
            returns = p.text.split('\n')
            if len(returns) == 2:
                self.uuid = returns[0]
                self.token = returns[1]
                return True
            else:
                print_error('Unable to parse play.opsoro uuid and token')
                return False


Play = _Play()
