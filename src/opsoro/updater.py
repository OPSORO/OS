"""
This module defines the interface for updating the robot.

.. autoclass:: _Updater
   :members:
   :undoc-members:
   :show-inheritance:
"""

from __future__ import division
from __future__ import with_statement

import sys
import re
from functools import partial

from git import Git, Repo
import os
import subprocess
import shutil
import stat

from opsoro.console_msg import *


class _Updater(object):
    def __init__(self):
        self.dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/'

        self.git = None
        self.repo = None
        try:
            self.git = Git(self.dir)
            self.repo = Repo(self.dir)
        except Exception as e:
            print_warning('Git repo error' + str(e))
            pass

    def get_current_branch(self):
        """
        Retrieves the current git branch of the repository.

        :return:    current git branch.
        :rtype:     string
        """
        if self.git is None:
            return False
        try:
            return str(self.repo.active_branch).split()[-1]
        except Exception as e:
            print_error("Failed to get current branch, is there a git repo setup?" + str(e))
            return ""

    def get_current_revision(self):
        """
        Retrieves the current git revision of the repository.

        :return:    current git revision.
        :rtype:     string
        """
        if self.git is None:
            return False
        try:
            # Request latest commit revision
            return str(self.git.log("--pretty=%h", "-1"))
        except Exception as e:
            print_error("Failed to get current revision, is there a git repo setup?" + str(e))
            return ""

    def get_remote_branches(self):
        """
        Retrieve all git branches of the repository.

        :return:    branches of the repository.
        :rtype:     list
        """
        if self.git is None:
            return False
        branches = []

        try:
            # Get all remote branches (not only local)
            returnvalue = self.git.ls_remote('--heads').split()

            # Strip data
            for i in range(len(returnvalue)):
                if i % 2 != 0:
                    # Get only branch name (last value)
                    branches.append(returnvalue[i].split("/")[-1])
        except Exception as e:
            print_warning("Failed to get remote branches, is there a git repo setup and do you have internet?" + str(e))
            pass

        return branches

    def is_update_available(self):
        """
        Checks git repository for available changes.

        :return:    True if update is available, False if the command failed or no update available.
        :rtype:     bool
        """
        if self.git is None:
            return False
        try:
            # Update local git data
            self.git.fetch()
        except Exception as e:
            print_error('Failed to fetch: ' + str(e))
            return False
        # Retrieve git remote <-> local difference status
        status = self.git.status()
        # easy check to see if local is behind
        if status.find('behind') > 0:
            return True
        return False

    def update(self):
        """
        Updates the opsoro software thru git
        """
        if self.git is None:
            return False
        # Create file to let deamon know it has to update before starting the server
        # file = open(self.dir + 'update.var', 'w+')

        backup_dir = '/home/pi/OPSORO/backup/'

        print('Updating...')
        if os.path.exists(backup_dir):
            # remove previous backup
            try:
                shutil.rmtree(backup_dir)
            except Exception as e:
                print_error('Remove backup failed: ' + str(e))
                pass

        try:
            shutil.copytree(self.dir, backup_dir)
        except Exception as e:
            print_error('Backup copy failed: ' + str(e))
            pass

        # Link git & update
        try:
            g = Git(self.dir)
            g.fetch('--all')
            g.reset('--hard', 'origin/' + g.branch().split()[-1])
            # g.pull()
        except Exception as e:
            print_error('Git failed to update: ' + str(e))
            pass

        # Set script executable for deamon
        try:
            st = os.stat(os.path.join(self.dir, 'run'))
            os.chmod(
                os.path.join(self.dir, 'run'), st.st_mode | stat.S_IXUSR |
                stat.S_IXGRP | stat.S_IXOTH)
        except Exception as e:
            print_error('Exec state set failed: ' + str(e))
            pass

        # Clear update var file
        # os.remove(os.path.join(self.dir, 'update.var'))

        # restart service
        command = ['/usr/sbin/service', 'opsoro', 'restart']
        #shell=FALSE for sudo to work.
        subprocess.call(command, shell=False)



        # python = sys.executable
        # os.execl(python, python, *sys.argv)


        # # Reboot system used for user development server run
        # os.system('/sbin/shutdown -r now')


Updater = _Updater()
