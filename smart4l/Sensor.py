# -*- coding: utf-8 -*-

import time

from smart4l.utils.RunnableObjectInterface import RunnableObjectInterface
from smart4l.utils.MeasureValue import MeasureValue

class Sensor(RunnableObjectInterface):
  def __init__(self, sensor_object, name, on_measure):
    self.sensor_object = sensor_object
    self.on_measure = on_measure
    self.name = name

  def do(self):
    measure = self.sensor_object.measure()
    self.on_measure(MeasureValue(id=self.name, date=str(time.time()), value=measure['value'], unit=measure['unit']))

  def stop(self):
    self.sensor_object.stop()

  def __str__(self):
    return f"{str(self.sensor_object)} : {self.name}"

  def __repr__(self):
    return str(self)
