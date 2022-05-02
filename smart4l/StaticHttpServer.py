# -*- coding: utf-8 -*-

import os
import signal
from subprocess import Popen, PIPE


class StaticHttpServer():
  def __init__(self) -> None:
  	self.running = False

  # Abstract method of RunnableObjectInterface
  def do(self):
    if self.running == False:
      os.popen('python3 -m http.server 8080 --directory /media/pi/SSD_Nvme/4lsylvie/')
      self.running = True

  # Abstract method of RunnableObjectInterface
  def stop(self):
    port = 8080
    process = Popen(["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    for process in str(stdout.decode("utf-8")).split("\n")[1:]:       
        data = [x for x in process.split(" ") if x != '']
        if (len(data) <= 1):
            continue

        os.kill(int(data[1]), signal.SIGKILL)
    
  def __str__(self):
    return f'StaticHttpServer host:localhost port:8080'

  def __repr__(self):
    return str(self)


if __name__ == '__main__':
  server = StaticHttpServer()
  try:
    server.do()
  except KeyboardInterrupt:
    server.stop()
