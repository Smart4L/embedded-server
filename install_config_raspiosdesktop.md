# Install Config Raspi OS Desktop
> cbarange | 2th June 2021
---

## Download and Flash Linux Operating System on raspi

### 1. Download Raspberry Pi OS with desktop *img* file [here](https://www.raspberrypi.org/software/operating-systems/)

### 2. Use [BalenaEtcher](https://www.balena.io/etcher/) for flash *img* file on SD-card

![](image/balenaetcher_flashos.png)

### 3. Add empty ssh file (without any extension) to Boot partition

![](image/ssh_file_bootpartition.png)

### 4. Insert SD card in raspberrypi and turn it on *(don't forget to plug ethernet cable)*

---
## Access to Raspi with SSH

### 1. Use [MobaXterm](https://mobaxterm.mobatek.net/download.html) *network scanner* tools to find Raspi IP

![](image/mobaxterm_networkscanner.png)

### 2. Use SSH to Access to Raspi with default user:*pi* and default password:*raspberry*

![](image/mobaxterm_sshuser.png)

### 3. Change default password for evident security reasons

![](image/change_password.png)

### 4. Enable SSH with command *sudo raspi-config* and menu *3 Interface Options > P2 SSH*

![](image/raspi_config.png)

---
## Update and Install usefull packages

### 1. Update raspi with command *sudo apt update && sudo apt upgrade*

![](image/update_raspi.png)

### 2. Install packages with commands 
```bash
sudo apt install -y git-all python3
```

---
## DS18B20 Temperature Sensor Sonde

### 1. DS18B20 Presentation 

The DS18B20 is a digital temperature sensor that provides 9 to 12 bit digital temperature measurements. Measurement temperature range is from -55°C to +125°C. The sensor communicates over One-Wire bus that requires only one data pin, power supply pin and ground pin for communication with a microcontroller. Each sensor has a unique 64 bit serial address, which allows multiple sensors to function on the same One-Wire bus. Thus, it is simple to use one microcontroller to control many sensors distributed over a large area. On raspi 1-Wire bus default pin is GPIO4 (pin 7)

![](image/ds18b20.png)

### 2. Connect DS18B20

![](image/ds18b20_raspi.png)

### 3. Enable One-Wire bus and get data

```bash
sudo raspi-config
# 3 Interface Options > P7 1-Wire > Enable
# You will be prompted to reboot the system, reboot raspi.
sudo modprobe w1-gpio
sudo modprobe w1-therm
# Try to get temp value from 1wire bus
cat /sys/bus/w1/devices/28-01193a459cac/temperature # 25875 - this is the temperature data in mili°C (Celsius) = 25,875°C
# 28-01193a459cac is the serial number of sensor, should be different for each sensor
```

### 4. Python implementation

```py
import os
import glob
import time

class DS18B20:
  base_dir = '/sys/bus/w1/devices/'

  def __init__(self, sensor_serial_id, sensor_label=None):
    self.sensor_serial_id = sensor_serial_id
    self.sensor_label = sensor_label
  
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
        return {
          'label':self.sensor_label,
          'serial_id':self.sensor_serial_id,
          'measure': str(float(open(f"{DS18B20.base_dir}{self.sensor_serial_id}/temperature").read())/1000),
          'symbol': '°C'
          }
      except Exception:
        raise Exception(f"Unable to access to {DS18B20.base_dir}{self.sensor_serial_id}/temperature file, please check if sensor_serial_id ({self.sensor_serial_id}) exists")

# Get all sensor serial id
#print(DS18B20.get_all_serial_id())

sensor=DS18B20('28-01193a2abb07')
print(sensor.measure())
```

---
## GY-61 ADXL335 Triple-axis Accelerometer

### 1. GY-61 ADXL335 Presentation 

The GY-61 accelerometer module is a three axis accelerometer sensor module based on the ADXL335 integrated circuit which reads X, Y and Z axis acceleration and converts them in analog voltages. Raspberry Pi can not read analog voltages, so the external analog to digital converter has to be used, like ADS1115 or PCF8591.

---
## GY-271 Compass Magnetic Module


---
## GY-521 MPU6050 3 Axes Gyroscope and Acceleration I2C

### 1. GY-521 MPU6050 Presentation 

The GY-521 is a module based on MPU6050 sensor chip which is a system that combines a 3-axis gyroscope, a 3-axis accelerometer and a digital thermometer. The module communicates through I2C protocol and it uses only two wires. Additional two wires are for power supply. The default I2C address is 0x68. By setting the AD0 pin to low, the modules I2C address can be changed to 0x69 which allows other devices to be connected with the I2C protocol. 

### 2. Connect GY-521 MPU6050

![](image/gy521_raspi.png)

### 3. Enable I2C bus and get data

```bash
sudo apt install -y python-smbus python3-smbus python-dev python3-dev i2c-tools
sudo pip3 install adafruit-circuitpython-mpu6050
sudo raspi-config # 3 Interface Options > P5 I2C > Enable
i2cdetect -y 1 # Result are 0x68
```
![](image/gy521_i2c_detect.png)

### 4. Python implementation

```py
import time
from math import atan2, degrees
import board
import busio
import adafruit_mpu6050



i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle

# Given an accelerometer sensor object return the inclination angles of X/Z and Y/Z
# Returns: tuple containing the two angles in degrees
def get_inclination(_sensor):
    x, y, z = _sensor.acceleration
    return vector_2_degrees(x, z), vector_2_degrees(y, z)



try:
  while True:
    angle_xz, angle_yz = get_inclination(sensor)
    print("XZ angle = {:6.2f}deg   YZ angle = {:6.2f}deg".format(angle_xz, angle_yz))

    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.gyro))
    print("Temperature: %.2f C"%mpu.temperature)
    print("-----")
    time.sleep(5)
except KeyboardInterrupt:
  print('\nScript end!')
```


# Bench Stress Test

```bash
sudo apt install -y sysbench
sysbench --num-threads=8 --test=cpu --cpu-max-prime=2000 run
```

# GPS

https://gitlab.com/scrobotics/balena-gps-tracker


# Amazon

Controlleur de charge https://www.amazon.fr/GEHOO-GH-7V-25-5V-R%C3%A9gulateur-Quadcopter/dp/B07DK6PF1V
Régulateur 5v : https://www.amazon.fr/AZDelivery-mt3608-DC-Adaptateur-dalimentation-Arduino/dp/B079H3YD8V
Régulateur 5v : https://www.amazon.fr/iHaospace-Converter-Regulator-Stabilizer-Adjustable/dp/B071H9NRTW
18650 : https://www.amazon.fr/kally-Rechargeables-Guirlandes-Lumineuses-T%C3%A9l%C3%A9commandes/dp/B093T6R3JZ/ref=sr_1_30


Charge controller 2A 2S: https://www.ebay.fr/itm/253084504432

Regulateur 12v 5v 3a: https://www.amazon.fr/Convertisseur-Regulateur-Adaptateur-dAlimentation-Smartphone/dp/B07H7J3HJS
https://www.amazon.fr/R%C3%A9gulateur-Tension-Alimentation-Convertisseur-Abaisseur/dp/B07PVSLYTS/ref=sr_1_19

GPS : https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/

https://www.waveshare.com/wiki/SIM7600G-H_4G_for_Jetson_Nano

https://www.youtube.com/watch?v=9sGrmQrrIGs

