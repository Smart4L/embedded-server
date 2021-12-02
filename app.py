#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import signal
import sys

from smart4l.Smart4L import Smart4L 

app = None

def main():
  logging.basicConfig(level=logging.INFO, datefmt='%d-%m-%Y %H:%M:%S') # Set logger level https://docs.python.org/3/library/logging.html#levels
  signal.signal(signal.SIGTERM, stop) # execute stop function when SIGTERM received
  global app
  app = Smart4L(database_file_path=os.path.dirname(__file__))

  try:    
    start()
  except KeyboardInterrupt:
    logging.warning('KeyboardInterrupt, smart4l will stopped')
  except:
    # Get exception that is currently being handled
    e = sys.exc_info()
    logging.exception(e)
    logging.exception(e.message)
  finally:
    stop()

def start():
  logging.info('Started, processing to starting check-up')
  # TODO:Checking for process already running with pid file
  logging.info('Check for PID lock file ✔')
  # Let's start application
  global app
  app.start()
  logging.info('Smart4L is now running... [quit]Press Ctrl+C')
  # Should stay in infinite loop to catch KeyboardInterrupt
  while True:
    pass

def stop():
  logging.info('Cleaning: GPIO, Memory, Web Client Connection...')
  global app
  app.stop()
  logging.info('Stopped !\n')

# Execute only if run as a script
if __name__ == "__main__":
    main()
else:
    logging.critical(f"{__name__} : must be run as a script\n")

