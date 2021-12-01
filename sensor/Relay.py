#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)





class Relay():
  def __init__(self, name, pin):
    self.pin = pin # 5 6 13 19
    self.name = name
    self.init_gpio()
    self.status = "off"
  
  def init_gpio(self):
    GPIO.setup(self.pin, GPIO.OUT)
    GPIO.output(self.pin, GPIO.HIGH)
  
  def on(self):
    GPIO.output(self.pin, GPIO.LOW)
    self.status = "on"
  
  def off(self):
    GPIO.output(self.pin, GPIO.HIGH)
    self.status = "off"
    
  def  get_status(self):
    return {"name": self.name, "status": self.status, "pin": self.pin}
  
  def stop(self):
    GPIO.cleanup()

  def __str__(self):
    return str({"name": self.name, "status": self.status, "pin": self.pin})    
  
  def __repr__(self):
    return str(self)

if __name__ == '__main__':
  relay = Relay('phare',5)
  while True:
    relay.on()
    sleep(1)
    relay.off()
    sleep(1)