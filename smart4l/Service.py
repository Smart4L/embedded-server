# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("Service")
from threading import Thread, Event
import sys

from smart4l.utils.RunnableObjectInterface import RunnableObjectInterface
from smart4l.utils.Status import Status

class Service(Thread):
  def __init__(self, runnable_object : RunnableObjectInterface, delay : int=0):
    Thread.__init__(self)
    self.delay_between_tasks = delay
    self.runnable_object = runnable_object

    self.status = Status.CREATED.value
    self.event_stop_service = Event()

  def run(self):
    logger.info(f'Service related to {repr(self.runnable_object)} starting... with interval delay:{self.delay_between_tasks}')
    self.status = Status.RUNNING.value
    while self.status == Status.RUNNING.value:
      try:
        self.runnable_object.do()
      except:
        logger.error(f"Unexpected error in Service {str(self.runnable_object)}:", sys.exc_info()[0])
        raise

      self.event_stop_service.wait(self.delay_between_tasks)

  def stop(self):
    logger.info(f'Service related to {repr(self.runnable_object)} stoping...')
    self.status = Status.TERMINATED.value
    self.event_stop_service.set()
    self.runnable_object.stop()
    logger.info(f'Service related to {repr(self.runnable_object)} Stopped !')

  def __str__(self):
    return str({"status":self.status, "runnable_object": repr(self.runnable_object), "delay": self.delay_between_tasks})

  def __repr__(self):
    return str(self)

  def serialize(self):
    return {"status":self.status, "runnable_object": repr(self.runnable_object), "delay": self.delay_between_tasks}