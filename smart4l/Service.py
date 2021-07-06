# -*- coding: utf-8 -*-

from threading import Thread, Event

class Service(Thread):
  def __init__(self, runnable_object : RunnableObjectInterface, delay : int=0):
    Thread.__init__(self)
    self.delay_between_tasks = delay
    self.runnable_object = runnable_object

    self.status = Status.CREATED.value
    self.event_stop_service = Event()

  def run(self):
    self.status = Status.RUNNING.value
    while self.status == Status.RUNNING.value:
      self.runnable_object.do()
      self.event_stop_service.wait(self.delay_between_tasks)

  def stop(self):
    self.status = Status.TERMINATED.value
    self.event_stop_service.set()
    self.runnable_object.stop()

  def __str__(self):
    return f"Current status: {self.status} - RunnableObject {str(self.runnable_object)} - Delay {str(self.delay_between_tasks)}"

  def __repr__(self):
    return str(self)