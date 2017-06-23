"""
This module defines the interface for reading and writing app files.

.. autoclass:: _Data
   :members:
   :undoc-members:
   :show-inheritance:
"""

import glob
import os
from functools import partial

from opsoro.apps import Apps
from opsoro.users import Users

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class _Data(object):
    def __init__(self):
        """
        Data class, used to read and write files.
        """
        pass

    def filelist(self, appname, extension='.*', trim_ext=True):
        """
        Get the list of files of a certain app, filtered by an extension.

        :param string appname:      current app name, to find the files of
        :param string extension:    extension of requested files

        :return:        files of an app.
        :rtype:         list
        """
        if not self._valid_parameters(appname, 'file' + extension):
            return None

        filenames = []

        filepaths = glob.glob(get_path('%s/*%s') % (appname, extension))
        for filepath in filepaths:
            if trim_ext:
                filenames.append(os.path.splitext(os.path.basename(filepath))[0])
            else:
                filenames.append(os.path.basename(filepath))
        filenames.sort()

        return filenames

    def read(self, appname, filename):
        """
        Read the data from a file.

        :param string appname:      current app name, to find the file of
        :param string filename:     name of the requested file

        :return:        file data.
        :rtype:         var
        """
        if not self._valid_parameters(appname, filename, True):
            return None

        data = None
        try:
            with open(get_path('%s/%s' % (appname, filename))) as f:
                data = f.read()
        except Exception as e:
            print_error(e)

        return data

    def write(self, appname, filename, data):
        """
        Write data to a file.

        :param string appname:      current app name, to find the file of
        :param string filename:     name of the requested file
        :param var data:            data to write to the file

        :return:        True if write was successfull.
        :rtype:         bool
        """
        if not self._valid_parameters(appname, filename, False):
            return False

        try:
            with open(get_path('%s/%s' % (appname, filename)), 'w') as f:
                f.write(data)
        except Exception as e:
            print_error(e)
            return False

        return True

    def delete(self, appname, filename):
        """
        Delete a file.

        :param string appname:      current app name, to find the file of
        :param string filename:     name of the requested file

        :return:        True if deletion was successfull.
        :rtype:         bool
        """
        if not self._valid_parameters(appname, filename, True):
            return False

        try:
            os.remove(get_path('%s/%s' % (appname, filename)))
        except Exception as e:
            print_error(e)
            return False

        return True

    def _valid_parameters(self, appname, filename='dummy.ext', file_required=False):
        """
        Check the validity of given parameters.

        :param string appname:      current app name, to find the file of
        :param string filename:     name of the requested file
        :param bool file_required:  does the file needs to exist

        :return:        True if all parameters are valid.
        :rtype:         bool
        """
        if appname not in Apps.apps:
            return False

        # If app-directory does not exist, create it
        if not os.path.isdir(get_path(appname)):
            os.makedirs(get_path(appname))

        if filename is None:
            return False

        # No path can be included in the filename
        if filename != os.path.basename(filename):
            return False

        # Filename should be at least 1 character long
        if len(os.path.splitext(filename)[0]) < 1:
            return False

        # If a file is required, check if it exists
        if file_required:
            if not os.path.exists(get_path('%s/%s' % (appname, filename))):
                return False

        return True


Data = _Data()
