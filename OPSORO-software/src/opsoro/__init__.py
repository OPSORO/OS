#!/usr/bin/env python

import signal
import sys
import logging
import logging.handlers
import random
import os
import tornado.log
import datetime

# from opsoro.server import Server

from opsoro.console_msg import *
from opsoro.server import Server


# Handle SIGTERM for graceful shutdown of daemon
def sigterm_handler(_signo, _stack_frame):
    print "SIGTERM received... Goodbye!"
    sys.exit(0)


LOG_FILE_DIR = '~/opsoro/log/'
if not os.path.exists(LOG_FILE_DIR):
    os.makedirs(LOG_FILE_DIR)

# Setup logging
LOG_FILENAME = LOG_FILE_DIR + str(datetime.date.today()) + ".log"
LOG_LEVEL = logging.DEBUG

tornado.log.enable_pretty_logging()
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(
    LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    signal.signal(signal.SIGTERM, sigterm_handler)
    print_info("OPSORO OS started...")
    app = Server()
    app.run()

# Initialization
if __name__ == "__main__":
    main()
