#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import time

class DS18B20():
  base_dir = '/sys/bus/w1/devices/'

  def __init__(self, id, sensor_serial_id):
    self.id_sensor = id
    self.sensor_serial_id = sensor_serial_id
    
  
  @staticmethod
  def get_all_serial_id():
    device_folder = glob.glob(DS18B20.base_dir + '28*')
    count_devices = len(device_folder)
    devices = list()
    i = 0
    while i < count_devices:
      devices.append(device_folder[i] + '/w1_slave')
      i += 1
    names = list()
    for i in range(count_devices):
      names.append(devices[i])
      temp = names[i][20:35]
      names[i] = temp
    return names

  def measure(self):
      try:
        return { "value": {"temperature" :str(float(open(f"{DS18B20.base_dir}{self.sensor_serial_id}/temperature").read())/1000)} }
      except Exception:
        raise Exception(f"Unable to access to {DS18B20.base_dir}{self.sensor_serial_id}/temperature file, please check if sensor_serial_id ({self.sensor_serial_id}) exists")


  def stop(self) -> None:
    pass

  def __str__(self):
    return f'Sensor:{self.id_sensor}'

  def __repr__(self):
    return str(self)



if __name__ == '__main__':
  # Get all sensor serial id
  print(DS18B20.get_all_serial_id())
  sensor=DS18B20('28-01193a2abb07', '28-01193a2abb07')
  try:
    while True:
      print(sensor.measure())
      time.sleep(1)
  except:
    print("KeyboardInterpute")

  
