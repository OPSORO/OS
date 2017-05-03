import os
from random import randint


# Helper classes to deal with login


class _User(object):
    def __init__(self):
        self.id = 'Guest'  # str(randint(0, 1000000))
        self.app = None
        self.name = ''
        self.authenticated = False
        self.admin = False
        self.token = os.urandom(24)

        self.id = self.token

        self.sockets = set()

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return not self.authenticated

    def get_id(self):
        return self.id

    @property
    def is_admin(self):
        return self.admin


class Admin(_User):
    def __init__(self):
        super(Admin, self).__init__()
        self.authenticated = True
        self.admin = True


class Play(_User):
    def __init__(self):
        super(Play, self).__init__()
        self.authenticated = True
        self.admin = False


class Guest(_User):
    def __init__(self):
        super(Guest, self).__init__()
        self.authenticated = False
        self.admin = False
