#!/usr/bin/env python

import signal
import sys
import logging
import logging.handlers
import random
import os
import tornado.log
import onoapplication
from consolemsg import *

# Handle SIGTERM for graceful shutdown of daemon
def sigterm_handler(_signo, _stack_frame):
	print "SIGTERM received... Goodbye!"
	sys.exit(0)

# Setup logging
LOG_FILENAME = "/tmp/OnoSW.log"
LOG_LEVEL = logging.DEBUG

tornado.log.enable_pretty_logging()
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialization
if __name__ == "__main__":
	signal.signal(signal.SIGTERM, sigterm_handler)

	print_info("OnoSW started...")
	app = onoapplication.OnoApplication()
	app.run()
