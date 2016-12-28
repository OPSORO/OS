from opsoro import stoppable_thread

class CSystem(object):
    def __init__(self):
        self.thread = Thread(target=self.update)
        pass

    def update(self):
        pass

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()
