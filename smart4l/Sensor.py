# -*- coding: utf-8 -*-

class Sensor(RunnableObjectInterface):
  def __init__(self, sensor_object, name, on_measure):
    self.sensor_object = sensor_object
    self.on_measure = on_measure
    self.name = name

  def do(self):
    self.on_measure(self.name, self.sensor_object.measure())        

  def stop(self):
    pass

  def __str__(self):
    return f"{str(self.sensor_object)} : {self.name}"

  def __repr__(self):
    return str(self)
