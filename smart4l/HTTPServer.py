# -*- coding: utf-8 -*-

import logging
import requests
from flask import Flask, jsonify, request, render_template
from utils.RunnableObjectInterface import RunnableObjectInterface

class HTTPServer(RunnableObjectInterface):
  def __init__(self, host, port):
    self.app = Flask(__name__)
    self.conf = {"host": host, "port": port}
    self.router()

  def router(self):
    self.app.add_url_rule('/', 'index', self.index)
    #self.app.add_url_rule('/service', 'service', self.service)
    #self.app.add_url_rule('/history', 'history', self.history)
    #self.app.add_url_rule('/log', 'log', self.log)
    self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)


  # Abstract method of RunnableObjectInterface
  def do(self):
    self.app.run(**self.conf)

  # Abstract method of RunnableObjectInterface
  def stop(self):
    requests.get(f"http://{self.conf.get('host')}:{self.conf.get('port')}/shutdown", verify=False)
    
  def index(self):
    return jsonify('Hello')

  # Must be call from HTTP request 👉 GET:http://domain/shutdown
  def shutdown(self):
    app_shutdown = request.environ.get('werkzeug.server.shutdown')
    if app_shutdown is None:
      raise RuntimeError("Http FlaskAPI can\'t be shutdown with this server version, check for WSGI version")
    else:
      app_shutdown()
    return "FlaskAPI shuting down ..."


