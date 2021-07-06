# -*- coding: utf-8 -*-

import logging
import requests
import json
from flask import Flask, jsonify, request, render_template
from smart4l.utils.RunnableObjectInterface import RunnableObjectInterface

class HTTPServer(RunnableObjectInterface):
  def __init__(self, host, port, services=None, measures=None) -> None:
    self.app = Flask(__name__)
    self.conf = {"host": host, "port": port}
    self.services = services
    self.measures = measures
    self.router()

  def router(self):
    self.app.add_url_rule('/', 'index', self.index)
    self.app.add_url_rule('/service', 'service', self.service)
    self.app.add_url_rule('/measure', 'measure', self.measure)
    #self.app.add_url_rule('/history', 'history', self.history)
    #self.app.add_url_rule('/log', 'log', self.log)
    self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)


  # Abstract method of RunnableObjectInterface
  def do(self):
    self.app.run(**self.conf)

  # Abstract method of RunnableObjectInterface
  def stop(self):
    requests.get(f"http://{self.conf.get('host')}:{self.conf.get('port')}/shutdown", verify=False)

  def __str__(self):
    return f'HTTPServer host:{self.conf.get("host")} port:{self.conf.get("port")}'

  def __repr__(self):
    return str(self)

  def index(self):
    return jsonify('Hello')

  def service(self):
    return jsonify([{"name":key,"service": value.serialize()} for key,value in self.services.items()]) # return {"HTTP":{"status":"RUNNING", "runnable_object": "HttpServer"},"WEBSocket":{"status":"STOPPED", "runnable_object": "WebSocketServerController"}} 

  def measure(self):
    return jsonify([{"name":key,"measure": value} for key,value in self.measures.items()])

  # Must be call from HTTP request 👉 GET:http://domain/shutdown
  def shutdown(self):
    app_shutdown = request.environ.get('werkzeug.server.shutdown')
    if app_shutdown is None:
      raise RuntimeError("Http FlaskAPI can\'t be shutdown with this server version, check for WSGI version")
    else:
      app_shutdown()
    return "FlaskAPI shuting down ..."


