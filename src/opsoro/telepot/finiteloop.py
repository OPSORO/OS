import traceback

from telepot import loop as old
import threading


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._shutdown = threading.Event()

    def stop(self):
        self._shutdown.set()


class StoppableDaemon(StoppableThread):
    def __init__(self, *args, **kwargs):
        super(StoppableDaemon, self).__init__(*args, **kwargs)
        self.daemon = True
