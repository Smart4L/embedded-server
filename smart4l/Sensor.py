# -*- coding: utf-8 -*-

import time
import logging
logger = logging.getLogger("SENSOR")
import sys

from smart4l.utils.RunnableObjectInterface import RunnableObjectInterface
from smart4l.utils.MeasureValue import MeasureValue
    

class Sensor(RunnableObjectInterface):
  def __init__(self, sensor_object, name, on_measure):
    self.sensor_object = sensor_object
    self.on_measure = on_measure
    self.name = name

  def do(self):
    try:
      measure = self.sensor_object.measure()
      if not measure==None:
        self.on_measure(MeasureValue(id=self.name, date=str(time.ctime()), value=measure['value'], unit=measure['unit']))
    except:
      logger.exception(f"Sensor {name} {str(sensor_object)} : {sys.exc_info()}")    

  def stop(self):
    self.sensor_object.stop()

  def __str__(self):
    return f"{str(self.sensor_object)} : {self.name}"

  def __repr__(self):
    return str(self)
