# -*- coding: utf-8 -*-

import requests
import json
import logging
logger = logging.getLogger("ExportData")

from smart4l.utils.RunnableObjectInterface import RunnableObjectInterface

class ExportData(RunnableObjectInterface):
  def __init__(self, measures, token):
    self.measures=measures
    self.token=token
    self.failed_request = []


  def do(self):
    # If data is empty don't insert in database
    if len(self.measures)==0:
      return
    url = "https://ycqc4785.directus.app/items/smart4l"
    headers = {
      'Authorization': f'Bearer {self.token}',
      'Content-Type': 'application/json'
    }
    try:
      for sensor_id, measure in self.measures.items():
        payload = json.dumps({"name":sensor_id, "date":measure['date'], "value":json.dumps(measure['value'])})
        response = requests.request("POST", url, headers=headers, data=payload)
      logger.info(f"ExportData: send {len(self.measures)} requests")      
    except:
      self.failed_request.append(payload)
      if(len(self.failed_request)>50):
        self.failed_request = self.failed_request[::2]
    try:
      for payload in self.failed_request:
        response = requests.request("POST", url, headers=headers, data=payload)
      logger.info(f"ExportData: resend {len(self.failed_request)} failed requests")
    except:
      pass

  def stop(self):
    pass

  def __str__(self):
    return f'ExportData: {self.token}'

  def __repr__(self):
    return str(self)
