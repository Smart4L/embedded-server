# -*- coding: utf-8 -*-
import asyncio
import logging

from smart4l.HTTPServer import HTTPServer
from smart4l.WebSocketServerController import WebSocketServerController
from smart4l.Service import Service
from smart4l.Sensor import Sensor
from sensor.SensorMock import SensorMock

class Smart4L():

  def __init__(self) -> None:
    self.services = {}
    self.last_measure = {}

    self.http_server = HTTPServer(host="0.0.0.0", port=8080, services=self.services, measures=self.last_measure)
    self.ws_server = WebSocketServerController(asyncio.get_event_loop(), host="0.0.0.0", port=8082)
    #self.persistence =
    #self.add_service("DB", Service(self.persistence, delay=20))

    self.add_service("HTTP", Service(self.http_server))
    self.add_service("WS_SERVER", Service(self.ws_server))
    self.add_service("MOCK_SENSOR_1", Service(Sensor(SensorMock(), name="MockSensor1", on_measure=self.update_data), delay=2)) 
    self.add_service("MOCK_SENSOR_2", Service(Sensor(SensorMock(), name="MockSensor2", on_measure=self.update_data), delay=2)) 


  def start(self) -> None:
    [service.start() for service_id, service in self.services.items() if not service.is_alive()]

  def stop(self) -> None:
    [service.stop() for service_id, service in self.services.items()]

  def reload_services(self) -> None:
    [service.start() for service_id, service in self.services.items() if not service.is_alive()]

  def add_service(self, service_id: str, service: Service) -> None:
    self.services[service_id]=service

  def update_data(self, uid, value) -> None:
    # If value has not changed exit
    if uid in self.last_measure.keys() and self.last_measure[uid] == value:
      return
    logging.info(f'New sensor measure from {uid}, value:{value}')
    self.ws_server.send_message(value)
    self.last_measure[uid] = value


  


