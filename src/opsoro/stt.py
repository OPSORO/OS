"""
This module defines the interface for communicating with the STT libraries.

.. autoclass:: _STT
   :members:
   :undoc-members:
   :show-inheritance:
"""
#!/usr/bin/env python
import sys
#
# import os
# import string
# from functools import partial
# import subprocess
# from opsoro.preferences import Preferences
#
# get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class _STT(object):
    def __init__(self):
        """
        STT class, used to convert speech to text.
        """


# Global instance that can be accessed by apps and scripts
STT = _STT()
