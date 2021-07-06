# -*- coding: utf-8 -*

from enum import Enum

class Status(Enum):
  CREATED = 'created'
  RUNNING = 'running'
  WAITING = 'waiting'
  BLOCKED = 'blocked'
  TERMINATED = 'terminated'
