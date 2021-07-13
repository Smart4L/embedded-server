# -*- coding: utf-8 -*-

import asyncio
import json
import websockets

from smart4l.WebSocketServer import WebSocketServer

class WebSocketServerController:
  def __init__(self, loop: asyncio.AbstractEventLoop, host:str, port:int, measures: dict):
    self.loop = loop
    self.ws_server = WebSocketServer(measures)
    self.conf = {"host": host, "port": port}

  def do(self,):
    asyncio.set_event_loop(self.loop)
    start_server = websockets.serve(self.ws_server.ws_handler, self.conf["host"], self.conf["port"])
    self.loop.run_until_complete(start_server)
    self.loop.run_forever()
  
  def stop(self):
    asyncio.run_coroutine_threadsafe(self.ws_server.close_all_connections(), self.loop)
    self.loop.stop()

  def send_message(self, message:str):
    asyncio.run_coroutine_threadsafe(self.ws_server.send_to_clients(str(message)), self.loop)

  def __str__(self):
    return f'WebSocketServerController host:{self.conf["host"]} port:{self.conf["port"]}'

  def __repr__(self):
    return str(self)

