# -*- coding: utf-8 -*-

import abc

class SensorInterface(abc.ABC):
  @abc.abstractmethod
  def measure(self):
    pass

  @abc.abstractmethod
  def stop(self):
    pass
