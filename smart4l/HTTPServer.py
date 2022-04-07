# -*- coding: utf-8 -*-

import logging
import requests
import json
from flask import Flask, jsonify, request, render_template, Response, send_file
from flask_cors import CORS, cross_origin

from smart4l.utils.RunnableObjectInterface import RunnableObjectInterface

class HTTPServer(RunnableObjectInterface):
  def __init__(self, host, port, services=None, measures=None, persistence=None, gyroscope=None, relays=None) -> None:
    self.app = Flask(__name__)
    CORS(self.app)
    self.conf = {"host": host, "port": port}
    self.services = services
    self.measures = measures
    self.persistence = persistence
    self.gyroscope = gyroscope
    self.relays = relays
    self.router()

  def router(self):
    self.app.add_url_rule('/', 'index', self.index)
    self.app.add_url_rule('/service', 'service', self.service)
    self.app.add_url_rule('/measure', 'measure', self.measure)
    self.app.add_url_rule('/history', 'history', self.history)
    self.app.add_url_rule('/reset-gyro', 'reset-gyro', self.reset_gyro)
    self.app.add_url_rule('/relay/<name>', 'relay_post', self.relay_post, methods = ['POST'])
    self.app.add_url_rule('/relay/<name>', 'relay_delete', self.relay_delete, methods = ['DELETE'])
    self.app.add_url_rule('/relay/<name>', 'relay_get', self.relay_get, methods = ['GET'])
    self.app.add_url_rule('/tile/<zoom>/<x>/<y>.png', 'tile', self.get_img)
    self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)
    #self.app.add_url_rule('/log', 'log', self.log)

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

  def history(self):
    return jsonify(self.persistence.history(request.args.get('limit'),request.args.get('offset')))

  def measure(self):
    return jsonify([{"name":key,"measure": value} for key,value in self.measures.items()])
  
  def reset_gyro(self):
    self.gyroscope.reset_gyro()
    return jsonify(self.gyroscope.measure())
  
  def relay_get(self, name):
    relay = next(relay for relay in self.relays if relay.name==name)    
    return jsonify(relay.get_status())
    
  def relay_post(self, name):
    relay = next(relay for relay in self.relays if relay.name==name)
    relay.on()
    return jsonify(relay.get_status()) 
  
  def relay_delete(self, name):
    relay = next(relay for relay in self.relays if relay.name==name)
    relay.off()
    return jsonify(relay.get_status()) 

  def get_img(zoom = None, x = None, y = None):
    if(os.path.isfile(f'tiles/{zoom}-{x}-{y}.png')):
        return send_file(f'tiles/{zoom}-{x}-{y}.png', mimetype='image/png')
        with open(f'tiles/{zoom}-{x}-{y}.png', 'r') as handler:
            return(handler)
    else:
        return send_file(f'tiles/{0}-{0}-{0}.png', mimetype='image/png')

  # Must be call from HTTP request 👉 GET:http://domain/shutdown
  def shutdown(self):
    app_shutdown = request.environ.get('werkzeug.server.shutdown')
    if app_shutdown is None:
      raise RuntimeError("Http FlaskAPI can\'t be shutdown with this server version, check for WSGI version")
    else:
      app_shutdown()
    return "FlaskAPI shuting down ..."


