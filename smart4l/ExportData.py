# -*- coding: utf-8 -*-

import requests
import json

from smart4l.utils.RunnableObjectInterface import RunnableObjectInterface

class ExportData(RunnableObjectInterface):
  def __init__(self, measures, token):
    self.measures=measures
    self.token=token
    logger.info(f'SInitializing connection to {self.database_file_path} database')
    

  def do(self):
    # If data is empty don't insert in database
    if len(self.measures)==0:
      return
    url = "https://cl1gdx4wn66024301s6jy7ujlrb-server-vn57etnuya-ue.a.run.app/api/smart4ls"    
    headers = {
      'Authorization': f'Bearer {self.token}',
      'Content-Type': 'application/json'
    }
    for sensor_id, measure in self.measures.items():
      json.dumps({"name":sensor_id, "date":measure['date'], "value":json.dumps(measure['value'])})
      response = requests.request("POST", url, headers=headers, data=payload)
    
    logger.info(f"ExportData: send {len(self.measures)} requests")

  def stop(self):
    pass

  def __str__(self):
    return f'ExportData: {self.database_file_path}'

  def __repr__(self):
    return str(self)