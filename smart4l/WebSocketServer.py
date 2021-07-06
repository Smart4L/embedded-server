# -*- coding: utf-8 -*-
import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol

class WebSocketServer():
  clients = set()
    
  # add client to clients list
  async def register(self, ws: WebSocketServerProtocol) -> None:
    self.clients.add(ws)
    logging.info(f"WebSocket client from {ws.remote_address} connects.")

  # remove client from clients list
  async def unregister(self, ws: WebSocketServerProtocol) -> None:
    await ws.close(1000,"Normal Closure")
    self.clients.remove(ws)
    logging.info(f"WebSocket client from {ws.remote_address} disconnects.")

  # send message to one client
  async def send_to_client(self, ws: WebSocketServerProtocol, message: str) -> None:
    await ws.send(message)

  # Send message to all clients
  async def send_to_clients(self, message: str) -> None:
    if self.clients:
      await asyncio.wait([client.send(message) for client in self.clients])
      logging.info(f'WebSocket Sent to clients {",".join([f"{client.remote_address[0]}:{client.remote_address[1]}" for client in self.clients])}, message: {message}')

  # Handle client connection
  async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
    await self.register(ws)
    try:
      # Start communication
      # TODO:Flush messages to the new client
      # await asyncio.wait([ self.send_to_client(ws, json.dumps( {"type": "UPDATE_SENSOR", "content": {"id": k,"value": v}})) for k,v in store_smart4l.last_measure.items()])
      await self.distribute(ws)
    finally:
      # Remove client from clients list
      await self.unregister(ws)

  # Waiting for client messages, that keep connection alive
  async def distribute(self, ws: WebSocketServerProtocol) -> None:
    async for message in ws:
      pass
      # await self.send_to_clients(message)

  # Close connection for all client in clients list 
  async def close_all_connections(self):
    logging.info(f'WebSocket close all connections')
    await asyncio.wait([self.unregister(client) for client in self.clients])
