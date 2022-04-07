#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

class ScreenBlanking():

  def __init__(self, id=None, pin=12) -> None:
    self.id_sensor = id
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=self.button_callback) # Setup event on pin 10 rising edge

  def wait_push(self):
    while True:
      time.sleep(0.3)

  def button_callback(self, channel):
    print(channel)

  def turn_on(self):
    pass
    # xset -display :0 dpms force on

  def turn_off(self):
    pass
    # xset -display :0 dpms force off

  def stop(self):
    GPIO.cleanup()

  def __str__(self):
    return f'Sensor:{self.id_sensor}'

  def __repr__(self):
    return str(self)

if __name__ == '__main__':
  sensor = ScreenBlanking()
  try:
    while True:
      print(sensor.wait_push())
      time.sleep(1)
  except Exception as error:
    print(error)

  



