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
## SIM7600X G-H 4G GPS HAT

### 1. SIM7600X G-H Presentation

J'ai acheté le modèle 4G LTE version globale (SIM7600G). Fonctionne bien sur un Raspberry Pi 3B+ mais la documentation officielle est un peu trop superficielle. La carte demande de la configuration sur l'OS (driver qmicli + wan interface) pour configurer notamment la réception 4G.
Je n'ai pas encore testé le GPS.
Nécessite des connaissances de base sur la liaison série UART et les commandes Hayes.
Je déconseille aux débutants.

### 2. Connect & Plug SIM7600X 

> Some nice video → https://www.youtube.com/watch?v=kwk3qzaIcCU

|Name|Area|Owner|
|--:|:--:|:--|
|GPS|Global|USA|
|GLONASS|Global|Russia|
|BeiDou|Global|China|
|Galileo|Global|Europe|
|NavIC|Regional|India|
|QZSS|Regional|Japan|


* Serial Output use NMEA 0183 Standard (Comma delimited ASCII text)
* Updated at rate of 1/sec
* Each line is called a "sentence" {TIME},{LONGITUDE},{LATITUDE},{NUMBER_OF_VISIBLE_SATELLITE},{ALTITUDE}



https://www.raspberrypi.org/forums/viewtopic.php?t=250657
https://eco-sensors.ch/router-wifi-4g-hotspot/
https://www.waveshare.com/wiki/SIM7600G-H_4G_DONGLE
https://www.waveshare.com/wiki/Raspberry_Pi_networked_via_RNDIS

Forum command list : https://techship.com/faq/basic-gnss-gps-usage-guide-for-simcom-sim7100-sim7500-sim7600-series-cellular-modules/
ALLER VOIR 👉 Wiki : https://www.waveshare.com/wiki/SIM7600G-H_4G_for_Jetson_Nano
http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/gsm.inc.php
https://www.waveshare.com/wiki/SIM800C_GSM/GPRS_HAT
https://www.waveshare.com/wiki/SIM7600E-H_4G_HAT
https://www.waveshare.com/wiki/SIM7600G-H_4G_HAT_(B)
https://gitlab.com/scrobotics/balena-gps-tracker
GPS : https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
https://www.waveshare.com/wiki/SIM7600G-H_4G_for_Jetson_Nano
https://www.youtube.com/watch?v=9sGrmQrrIGs


**LOOKING FOR**
```bash

cd /home/pi/SIM7000X-4G-HAT-Demo/Raspberry/c
sudo ./sim7600_4G_hat_init

```

Connect the  Data 1 and Data 2  port  of  the modem to the PC using a micro USB cable.
* Data 1 - AT command port for accessing AT commands.
* Data 2 – Data port for accessing Internet , Audio, Calling and SMS, GPS.

Baudrate = 115200

```bash

sudo lsusb # Show USB devices, looking for CygnalIntegratedProduct CP2102/CP2109 UART Bridge Controlleur



# - Install GPS UI Tool -
sudo apt install -y gpsd gpsd-clients
sudo systemctl stop gpsd.socket # Stop it to disable
sudo systemctl disable gpsd.socket # Free serial port
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock # Manually start GPSD and connect to GPS on USB0
#sudo gpsd /dev/ttyUSB2 -F /var/run/gpsd.sock
cgps -s # Run GPSD Display
sudo killall gpsd

# - Install serial tool -
sudo apt-get install -y minicom # Testing AT command 
sudo minicom -D /dev/ttyUSB2

# - Install GSM tools -
sudo apt install -y libqmi-utils udhcpc
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode='online'
sudo qmicli -d /dev/cdc-wdm0 --dms-get-operating-mode # Get online status
sudo qmicli -d /dev/cdc-wdm0 --nas-get-signal-strength # Get Signal  strength quality
sudo qmicli -d /dev/cdc-wdm0 --nas-get-home-network # Get Carrier name
sudo ip link set wwan0 down
echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set wwan0 up
#sudo qmicli --device=/dev/cdc-wdm0 --device-open-proxy --wds-start-network="ip-type=4,apn=mmsfree" --client-no-release-cid
sudo qmicli --device=/dev/cdc-wdm0 --device-open-proxy --wds-start-network="ip-type=4,apn=orange,username=orange,password=orange" --client-no-release-cid
sudo udhcpc -i wwan0
ifconfig wwan0 # Check connection and get public ip
ifconfig # locate usb0 interface or alternative
sudo dhclient -v usb0
sudo dhclient -v wwan0


# sudo ip link set wwan0 up
# sudo udhcpc -i wwan0
# ip a s wwan0

# - Configure Serial -
sudo raspi-config # Interface>Disable Serial Shell & Enable Serial Port 
nano /boot/config.txt # Add
# enable_uart=1
# dtoverlay=pi3-disable-bt
nano /boot/cmdline.txt # Remove
# console=ttyAMA0,115200 & kgdboc=ttyAMA0,115200

# - Configure serial port for GY-NEO6MV2 -
stty -F /dev/ttyAMA0 9600
cat /dev/ttyAMA0 # Get GPS data
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock # Start viewer tool
cgps -s # Open viewer tool

# - Use AT command -
ls /dev/ttyUSB*
sudo minicom -D /dev/ttyUSB2
AT+CGMI # Manufacturer identification
AT+CGMM # Model identification  
AT+CGMR # Revision identification 
AT+CPIN=1234 # Unlock sim card with pin code
AT+CSPN? # Get service provider name from SIM

# - Configure APN (default is valid not necessary) -
AT
AT+SETAPN="providerapn"
AT+SETUSER="provideruser"
AT+SETPWD="providerpassword"
AT+SAVE
# - Send sms -
AT+CMGF=1 # Enable SMS text mode
AT+CMGF=? # Should output +CMGF: (0,1)
AT+CSCA? # Display Server Center Adress
# AT+CSCA="+33695000695" # DON'T Change it, default is valid or note default somewhere not like me...
AT+CMGS="+33695360970" # Send text message use CTRL+Z to valid message
# - Phone call -
AT+CGREG? # Should +CGREG: 0,1 The device return that is registred in the home network
AT+COPS? # Verifying the network registration status
AT+CSQ # Check sign quality
ATD33650520266;
AT+CHUP # Hang up current call or use ATH
ATDL # Call the last dialled number
# - GPS -
AT+CGPS=1 # Turn on power of GPS, AT+CGPSHOT Hot Start GPS 
# (Wait for the GPS to get the position) if you use script insert WAIT=15 command here (wait for 15sec) make sur antenna is outside
AT+CGPSINFO # Get GPS fixed position information
AT+CGPS=0 # Turn off power of GPS
AT+CGPSAUTO? # Start GPS automatic: 0 Non-Automatic 1 Automatic

# - Test internet connection -
ifconfig -a # Looking for WWAN0 interface
pip3 install speedtest_cli
speedtest # or use speedtest_cli
```




### 3. Configure

### 4. Get Data

---
## ICQUANZX GY-NEO6MV2 NEO-6M Module contrôleur de vol GPS 

```bash
sudo raspi-config # Enable Serial 
cat /dev/ttyAMA0

```

---
## SSH1106 GME12864 - 70 Ecran OLED I2C 128x64 Pixel

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

# Camera

doc IR mode : https://www.waveshare.com/wiki/RPi_IR-CUT_Camera_(B)
```bash
sudo nano /boot/config.txt
disable_camera_led=1
# Or GPIO port on camera : GPIO logic level. (HIGH --> Normal Mode, LOW --> Night-vision Mode)
```

# Edit file thourgth SSH

https://www.martinrowan.co.uk/2015/07/live-editing-raspberry-pi-files-remotely-windows-pc-using-sublime-text-rsub-putty/

```bash
ssh -R 52698:localhost:52698 pi@192.168.1.36

rsub somefile.txt
```


# Amazon

Controlleur de charge https://www.amazon.fr/GEHOO-GH-7V-25-5V-R%C3%A9gulateur-Quadcopter/dp/B07DK6PF1V
Régulateur 5v : https://www.amazon.fr/AZDelivery-mt3608-DC-Adaptateur-dalimentation-Arduino/dp/B079H3YD8V
Régulateur 5v : https://www.amazon.fr/iHaospace-Converter-Regulator-Stabilizer-Adjustable/dp/B071H9NRTW
18650 : https://www.amazon.fr/kally-Rechargeables-Guirlandes-Lumineuses-T%C3%A9l%C3%A9commandes/dp/B093T6R3JZ/ref=sr_1_30


Charge controller 2A 2S: https://www.ebay.fr/itm/253084504432

Regulateur 12v 5v 3a: https://www.amazon.fr/Convertisseur-Regulateur-Adaptateur-dAlimentation-Smartphone/dp/B07H7J3HJS
https://www.amazon.fr/R%C3%A9gulateur-Tension-Alimentation-Convertisseur-Abaisseur/dp/B07PVSLYTS/ref=sr_1_19



https://wiki.52pi.com/index.php/UPS_Plus_SKU:_EP-0136
https://www.amazon.fr/gp/product/B08W3YS58J/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1

