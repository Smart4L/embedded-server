# -*- coding: utf-8 -*

import abc

class RunnableObjectInterface(abc.ABC):
  @abc.abstractmethod
  def do(self):
    pass

  @abc.abstractmethod
  def stop(self):
    pass
