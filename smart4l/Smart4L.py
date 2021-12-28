# -*- coding: utf-8 -*-
import asyncio
import logging
import json
from smart4l.HTTPServer import HTTPServer
from smart4l.WebSocketServerController import WebSocketServerController
from smart4l.Service import Service
from smart4l.Sensor import Sensor
from smart4l.Persistence import Persistence
from smart4l.utils.MeasureValue import MeasureValue
from sensor.SensorMock import SensorMock, SensorMockJson
from sensor.SIM7600G_H_GPS import SIM7600G_H_GPS
from sensor.GY521_MPU6050 import GY521_MPU6050
from sensor.DS18B20 import DS18B20
from sensor.DHT11 import DHT11
from sensor.GY271 import GY271
from sensor.BMP280 import BMP280
from sensor.Relay import Relay

class Smart4L():

  def __init__(self, database_file_path) -> None:
    self.services = {}
    self.last_measure = {}
    gyroscope = GY521_MPU6050(id='GY521_MPU6050')
    relay_phare = Relay('phare', 5)
    relay_klaxon = Relay('klaxon', 6)
    relay_ventilateur1 = Relay('ventilateur1', 13)
    relay_ventilateur2 = Relay('ventilateur2', 19)
    
    self.persistence = Persistence(database_file_path=database_file_path, measures=self.last_measure)
    self.http_server = HTTPServer(host="0.0.0.0", port=8080, services=self.services, measures=self.last_measure, persistence=self.persistence, gyroscope=gyroscope, relays=[relay_phare, relay_klaxon, relay_ventilateur1, relay_ventilateur2])
    self.ws_server = WebSocketServerController(asyncio.get_event_loop(), host="0.0.0.0", port=8082, measures=self.last_measure)
    
    self.add_service("DB", Service(self.persistence, delay=20))
    self.add_service("HTTP", Service(self.http_server))
    self.add_service("WS_SERVER", Service(self.ws_server))
    
    self.add_service("DS18B20_28-01193a459cac", Service(Sensor(DS18B20(id="28-01193a459cac", sensor_serial_id="28-01193a459cac"), name="DS18B20_28-01193a459cac", on_measure=self.update_data), delay=1)) 
    self.add_service("DS18B20_28-01193a2abb07", Service(Sensor(DS18B20(id="28-01193a2abb07", sensor_serial_id="28-01193a2abb07"), name="DS18B20_28-01193a2abb07", on_measure=self.update_data), delay=1)) 
    self.add_service("GY271", Service(Sensor(GY271(id='GY271'), name="GY271", on_measure=self.update_data), delay=0.2)) 
    self.add_service("BMP280", Service(Sensor(BMP280(id='BMP280'), name="BMP280", on_measure=self.update_data), delay=3)) 
    self.add_service("DHT11_25", Service(Sensor(DHT11(id='DHT11_25'), name="DHT11_25", on_measure=self.update_data), delay=1)) 
    self.add_service("SIM7600G_H_GPS", Service(Sensor(SIM7600G_H_GPS(id="SIM7600G_H_GPS"), name="SIM7600G_H_GPS", on_measure=self.update_data), delay=0.3)) 
    self.add_service("GY521_MPU6050", Service(Sensor(gyroscope, name="GY521_MPU6050", on_measure=self.update_data), delay=0.2)) 


  def start(self) -> None:
    [service.start() for service_id, service in self.services.items() if not service.is_alive()]

  def stop(self) -> None:
    [service.stop() for service_id, service in self.services.items()]

  def reload_services(self) -> None:
    [service.start() for service_id, service in self.services.items() if not service.is_alive()]

  def add_service(self, service_id: str, service: Service) -> None:
    self.services[service_id]=service

  def update_data(self, data: MeasureValue) -> None:
    # If value has not changed exit
    data_json = json.dumps(data.__dict__)
    data_dict_without_id = data.__dict__.copy()
    del data_dict_without_id['id']

    if data.id in self.last_measure.keys() and self.last_measure[data.id] == data_dict_without_id:
      return

    logging.info(f'New sensor measure {data_json}')
    self.ws_server.send_message(data_json)
    self.last_measure[data.id] = data_dict_without_id
