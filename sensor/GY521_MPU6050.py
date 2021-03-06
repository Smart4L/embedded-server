#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from math import atan2, degrees
import board
import busio
import adafruit_mpu6050


class GY521_MPU6050():
  def __init__(self, id=None, address=0x68) -> None:
    self.id_sensor = id
    self.i2c = busio.I2C(board.SCL, board.SDA)
    self.mpu = adafruit_mpu6050.MPU6050(self.i2c, address=address)
    self.fix_gyro = {'X':0, 'Y':0, 'Z': 0}

  def reset_gyro(self):
    angle_xz, angle_yz = self.get_inclination(self.mpu)
    inclinaisons = "%.2f,%.2f,%.2f"%(self.mpu.acceleration)
    inclinaisons = inclinaisons.split(',')
    inclinaison = {
      'X': float(inclinaisons[0]), 
      'Y': float(inclinaisons[1]),
      'Z': float(inclinaisons[2])
      }
    self.fix_gyro = {'X':inclinaison['X'], 'Y':inclinaison['Y'], 'Z':inclinaison['Z']}


  def vector_2_degrees(self, x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
      angle += 360
    return angle

  # Given an accelerometer sensor object return the inclination angles of X/Z and Y/Z
  # Returns: tuple containing the two angles in degrees
  def get_inclination(self, _sensor):
    x, y, z = _sensor.acceleration
    return self.vector_2_degrees(x, z), self.vector_2_degrees(y, z)


  def measure(self) -> dict:
    try:
      angle_xz, angle_yz = self.get_inclination(self.mpu)
      inclinaisons = "%.2f,%.2f,%.2f"%(self.mpu.acceleration)
      inclinaisons = inclinaisons.split(',')
      inclinaison = {
        'X': float(inclinaisons[0])-self.fix_gyro['X'], 
        'Y': float(inclinaisons[1])-self.fix_gyro['Y'],
        'Z': float(inclinaisons[2])-self.fix_gyro['Z']
        }
    except:
      return None

    return {'value':{'acceleration': "{:6.2f},{:6.2f}".format(angle_xz, angle_yz), 'gyroscope': inclinaison, 'temperature': "%.2f"%self.mpu.temperature}}

  def stop(self) -> None:
    pass

  def __str__(self):
    return f'Sensor:{self.id_sensor}'

  def __repr__(self):
    return str(self)


if __name__ == '__main__':
  sensor = GY521_MPU6050("GY521_MPU6050")
  try:
    while True:
      print(sensor.measure())
      time.sleep(1)
  except Exception as e:
    print(e)

