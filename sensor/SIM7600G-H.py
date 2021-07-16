#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# pip3 install pynmea2

import serial
import time

class SIM7600G_H():
  def __init__(self, id=None, serial="/dev/ttyUSB2") -> None:
    self.id_sensor = id
    self.serial = serial.Serial(serial, 115200)


  def measure(self) -> dict:
    return {'unit':'°', 'value':{'latitude':90000,'longitude':1000}}

  def stop(self) -> None:
    pass

  def __str__(self):
    return f'Sensor:{self.id_sensor}'

  def __repr__(self):
    return str(self)


if __name__ == "__main__":
  SIM7600G_H = SIM7600G_H()
  while True:
    print(SIM7600G_H.measure())
    time.sleep(5)








# Start device
# Verifie que personne n'est connecté sur le port
# Deconnecte les gens sur le port
# Enable GPS
# Get GPS
# Disable GPS








import serial
import pynmea2
port = "/dev/ttyUSB2"

def parseGPS(str):
  if str.find('GGA') > 0:
    msg = pynmea2.parse(str)
    print(f"Timestamp: {msg.timestamp} -- Lat: {msg.lat} {msg.lat_dir} -- Lon: {msg.lon} {msg.lon_dir} -- Altitude: {msg.altitude} {msg.altitude_units} -- Satellites: {msg.num_sats}")
    


serialPort = serial.Serial(port, baudrate = 115200, timeout = 0.5)
while True:
  str = serialPort.readline()
  parseGPS(str)