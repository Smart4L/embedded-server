#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("SIM7600G_H_GPS")
import re
import serial
import time
from pynmeagps import NMEAMessage, GET

class SIM7600G_H_GPS():
  def __init__(self, id=None, serial_port="/dev/ttyUSB2", timeout=0.5) -> None:
    self.id_sensor = id
    self.port = serial_port
    self.serial = None
    self.open_serial()
    self.timeout = timeout
    if not self.check_gps_power_status() in '+CGPS: 1,1':
      self.enable_gps()


  def measure(self) -> dict:
    # [<lat>],[<N/S>],[<log>],[<E/W>],[<date>],[<UTC time>],[<alt>],[<speed>],[<course>]
    # <lat> Latitude of current position. Output format is ddmm.mmmmmm
    # <N/S> N/S Indicator, N=north or S=south
    # <log> Longitude of current position. Output format is dddmm.mmmmmm
    # <E/W> E/W Indicator, E=east or W=west
    # <date> Date. Output format is ddmmyy
    # <UTC time> UTC Time. Output format is hhmmss.s
    # <alt> MSL Altitude. Unit is meters.
    # <speed> Speed Over Ground. Unit is knots.
    # <course> Course. Degrees.
    # <time> The range is 0-255, unit is second, after set <time> will report the GPS information every the seconds.
    try:
      cgpsinfo = self.get_current_location()
      if re.match("\r?\n?AT\+CGPSINFO\r*\n*\+CGPSINFO: [0-9]+\.[0-9]+,[NS],[0-9]+\.[0-9]+,[EW].*", cgpsinfo):
        cgpsinfo = cgpsinfo.split('\r\n')[1].split(' ')[1].split(',')
        # lat = float(cgpsinfo[0])/100
        # log = float(cgpsinfo[2])/100
        pyld = [cgpsinfo[0],cgpsinfo[1],cgpsinfo[2],cgpsinfo[3], cgpsinfo[5], 'A', 'A']
        msg = NMEAMessage('GN', 'GLL', GET, payload=pyld)
        return {'unit':'°', 'value':{'latitude': msg.lat,'longitude': msg.lon , 'altitude': float(cgpsinfo[6]), 'speed':f"{cgpsinfo[7]}"}}
        # return {'unit':'°', 'value':{'latitude': lat *-1 if cgpsinfo[1]=="S" else lat,'longitude': log *-1 if cgpsinfo[3]=="W" else log, 'altitude': float(cgpsinfo[6]), 'speed':f"{cgpsinfo[7]} knots"}}
      else:
        return None
    except:
      self.open_serial()
      raise

  def open_serial(self):
    try:
      if not self.serial == None:
        self.serial.close()
    except:
      pass

    try:
      self.serial = serial.Serial(self.port, 115200)
      self.serial.flushInput()
    except:
      logger.error(f"Unable to open serial connection on {self.port}, try with /dev/ttyS0")
      try:
        self.serial = serial.Serial("/dev/ttyS0", 115200)
        self.serial.flushInput()
      except:
        logger.error(f"GPS Serial connection failed on port /dev/ttyS0 and {self.port}")





  def send_serial_command(self, command):
    self.serial.write((command+'\r\n').encode())
    time.sleep(self.timeout)
    return self.serial.read(self.serial.inWaiting()).decode()

  def check_gps_power_status(self):
    return self.send_serial_command("AT+CGPS?")   

  def enable_gps(self):
    return self.send_serial_command("AT+CGPS=1")

  def disable_gps(self):
    return self.send_serial_command("AT+CGPS=0")    
    
  def check_for_at_command_trought_serial_connection(self):
    self.serial.write(("AT"+'\r\n').encode())
    time.sleep(self.timeout)
    if self.serial.inWaiting():
      return self.serial.read(self.serial.inWaiting()).decode() # Should output OK
    else:
      return f"Unable to send AT command, check for serial connection and make sure that no one already listen on {self.port}"
  
  def get_current_location(self) -> str:
    interation_counter=0
    buf = ''
    while interation_counter<10 and (buf in '+CGPSINFO: ,,,,,,,,' or buf ==''):
      if interation_counter!=0:
        time.sleep(5) # Waiting for GPS signal

      self.serial.write(("AT+CGPSINFO"+'\r\n').encode())
            
      waiting_counter=0 # Some times CGPSINFO command result is slow to being retrieved
      while waiting_counter<5 and not self.serial.inWaiting():
        time.sleep(self.timeout)
        waiting_counter+=1

      buf = self.serial.read(self.serial.inWaiting()).decode()
      
      

      interation_counter+=1      

    # +CGPSINFO: [lat],[N/S],[log],[E/W],[date],[UTC time],[alt],[speed],[course]
    return buf

  def stop(self) -> None:
    self.disable_gps()
    self.serial.close()

  def __str__(self):
    return f'Sensor:{self.id_sensor}'

  def __repr__(self):
    return str(self)


if __name__ == "__main__":
  SIM7600G_H_GPS = SIM7600G_H_GPS()

  print("Check for command \"AT\", sould output \"OK\":")
  print(SIM7600G_H_GPS.check_for_at_command_trought_serial_connection())

  print("\nCheck GPS Power Status")
  print(SIM7600G_H_GPS.check_gps_power_status())
  

  counter=0
  while counter<5:
    print(f"\nGet location {counter+1}/5")
    print(SIM7600G_H_GPS.measure())
    counter+=1
  
  print("\nStop GPS and Serial")
  SIM7600G_H_GPS.stop()
  
