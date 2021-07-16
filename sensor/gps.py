#!/usr/bin/python

import serial
import time
import pynmea2

ser = serial.Serial('/dev/ttyUSB2',115200)
ser.flushInput()

ser.write(("AT"+'\r\n').encode())
time.sleep(1)
if ser.inWaiting():
  time.sleep(0.01)
  output = ser.read(ser.inWaiting())
  print(output.decode().split('\r\n'))
  
  ser.write(("AT+CGPS=1"+'\r\n').encode())
  time.sleep(0.01)
  output = ser.read(ser.inWaiting())
  print(output.decode().split('\r\n'))

  cpt=0
  buf = ''
  while buf == '+CGPSINFO: ,,,,,,,,' or buf =='':
    time.sleep(5)
    ser.write(("AT+CGPSINFO"+'\r\n').encode())
    time.sleep(0.01)
    output = ser.read(ser.inWaiting())
    print(output.decode().split('\r\n'))
    buf = output.decode().split('\r\n')[1]
    print(buf)
    cpt+=1
    if cpt>10:
      break
      
  print(f"RESULT: {pynmea2.parse(buf)}")

  ser.write(("AT+CGPS=0"+'\r\n').encode())
  time.sleep(0.01)
  output = ser.read(ser.inWaiting())
  print(output.decode().split('\r\n'))
  
else:
  print("Impossible d'acceder au port serial")

ser.close()



# def sendAt(command,back,timeout):
#   #rec_buff = ''
#   ser.write((command+'\r\n').encode())
#   time.sleep(timeout)
#   if ser.inWaiting():
#     time.sleep(0.01)
#     rec_buff = ser.read(ser.inWaiting())
#   if rec_buff != '':
#     if back not in rec_buff.decode():
#       print(command + ' ERROR')
#       print(command + ' back:\t' + rec_buff.decode())
#       return 0
#     else:
#       print(rec_buff.decode())
#       return 1
#   else:
#     print('GPS is not ready')
#     return 0

# def getGpsPosition():
#   rec_null = True
#   answer = 0
#   print('Start GPS session...')
#   rec_buff = ''
#   sendAt('AT+CGPS=1','OK',1)
#   time.sleep(2)
#   while rec_null:
#     answer = sendAt('AT+CGPSINFO','+CGPSINFO: ',1)
#     if 1 == answer:
#       answer = 0
#       if ',,,,,,,,' in rec_buff:
#           print('GPS is not ready,wait 10 seconds')
#           rec_null = False
#           time.sleep(10)
#     else:
#       print('error %d'%answer)
#       rec_buff = ''
#       sendAt('AT+CGPS=0','OK',1)
#       return False
#     time.sleep(1.5)
#     #整理数据内容


# def checkStart():
#   while True:
#       ser.write( ('AT\r\n').encode() )
#       time.sleep(0.1);
#       if ser.inWaiting():
#           time.sleep(0.01)
#           output = ser.read(ser.inWaiting()).decode()
#           print( 'try to start\n' + recBuff.decode() )
#           if 'OK' in recBuff.decode():
#             recBuff = ''
#             return
#       else:
#           powerOn()
#           time.sleep(1)

# try:
#   #checkStart()
#   getGpsPosition()
#   powerDown()
# except:
#   if ser != None:
#     ser.close()
#   powerDown()
  
# if ser != None:
#   ser.close()
        
