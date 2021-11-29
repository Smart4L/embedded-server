#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# pip3 install adafruit-circuitpython-dht
# sudo apt-get install libgpiod2

import time
import board
import adafruit_dht

class DHT11():
  def __init__(self, id=None, pin=board.D25) -> None:
    self.id_sensor = id
    self.dht_device = adafruit_dht.DHT11(pin) # BCM 25 / name : GPIO 6 / Phy 22

  def measure(self) -> dict:
    try:
        temperature_c = self.dht_device.temperature #"{:.1f}"%
        humidity = self.dht_device.humidity
        return {
          "temperature": { "value":temperature_c, "unit":"°C"},
          "humidity" : { "value":humidity, "unit":"%" }
        }
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    except Exception as error:
        self.dht_device.exit()
        raise error

  def stop(self) -> None:
    self.dht_device.exit()

  def __str__(self):
    return f'Sensor:{self.id_sensor}'

  def __repr__(self):
    return str(self)

if __name__ == '__main__':
  sensor = DHT11()
  try:
    while True:
      print(sensor.measure())
      time.sleep(1)
  except:
    print("KeyboardInterpute")

  