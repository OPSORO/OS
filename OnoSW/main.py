#!/usr/bin/env python

import signal
import sys
import logging
import logging.handlers
import random
import os
import onoapplication

# Handle SIGTERM for graceful shutdown of daemon
def sigterm_handler(_signo, _stack_frame):
	print "SIGTERM received... Goodbye!"
	sys.exit(0)

# Setup logging
LOG_FILENAME = "/tmp/OnoSW.log"
LOG_LEVEL = logging.INFO

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class OnoLogger(object):
	def __init__(self, logger, level, oldstream=None):
		self.logger = logger
		self.level = level
		self.oldstream = oldstream

	def write(self, message):
		if self.oldstream:
			self.oldstream.write(message)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())

sys.stdout = OnoLogger(logger, logging.INFO, sys.stdout)
sys.stderr = OnoLogger(logger, logging.ERROR, sys.stderr)

# Initialization
if __name__ == '__main__':
	signal.signal(signal.SIGTERM, sigterm_handler)
	#signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # Fix for "IOError: [Errno 32] Broken pipe"

	print "Ono SW started..."
	app = onoapplication.OnoApplication()
	app.run()
