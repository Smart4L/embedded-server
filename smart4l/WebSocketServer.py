# -*- coding: utf-8 -*-
import asyncio
import json
import logging
logger = logging.getLogger("WebSocketServer")
import websockets
from websockets import WebSocketServerProtocol

class WebSocketServer():
  clients = set()
    
  def __init__(self, measures):
    self.measures = measures

  # add client to clients list
  async def register(self, ws: WebSocketServerProtocol) -> None:
    self.clients.add(ws)
    logger.info(f"WebSocket client from {ws.remote_address} connects.")

  # remove client from clients list
  async def unregister(self, ws: WebSocketServerProtocol) -> None:
    await ws.close(1000,"Normal Closure")
    self.clients.remove(ws)
    logger.info(f"WebSocket client from {ws.remote_address} disconnects.")

  # send message to one client
  async def send_to_client(self, ws: WebSocketServerProtocol, message: str) -> None:
    await ws.send(message)

  # Send message to all clients
  async def send_to_clients(self, message: str) -> None:
    if self.clients:
      await asyncio.wait([client.send(message) for client in self.clients])
      #logger.info(f'WebSocket Sent to clients {",".join([f"{client.remote_address[0]}:{client.remote_address[1]}" for client in self.clients])}, message: {message}')

  # Handle client connection
  async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
    await self.register(ws)
    try:
      # Flush current measures to the new client
      await asyncio.wait([ self.send_to_client(ws, json.dumps({"id":id, **data})) for id,data in self.measures.items()])
      await self.distribute(ws)
    except:
      pass
    finally:
      # Remove client from clients list
      await self.unregister(ws)

  # Waiting for client messages, that keep connection alive
  async def distribute(self, ws: WebSocketServerProtocol) -> None:
    try:
      async for message in ws:
        pass
      # await self.send_to_clients(message)
    except websockets.ConnectionClosed:
      raise   

  # Close connection for all client in clients list 
  async def close_all_connections(self):
    logger.info(f'WebSocket close all connections')
    await asyncio.wait([self.unregister(client) for client in self.clients])
