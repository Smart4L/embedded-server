# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("Persistence")
import json
import sqlite3
import time
from smart4l.utils.RunnableObjectInterface import RunnableObjectInterface

class Persistence(RunnableObjectInterface):
  def __init__(self, database_file_path, measures):
    self.database_file_path=f'{database_file_path}/smart4l.db'
    self.measures=measures
    db = sqlite3.connect(self.database_file_path)
    logger.info(f'Initializing connection to {self.database_file_path} database')
    cursor = db.cursor()
    cursor.execute("create table if not exists smart4l(id varchar(50), date varchar(50), unit varchar(50), value json)")
    cursor.close()
    db.commit()
    db.close()

  def do(self):
    # TODO DB registration
    db = sqlite3.connect(self.database_file_path)
    cursor = db.cursor()
    [cursor.execute('insert into smart4l(id, date, unit, value) values(?,?,?,?)', [sensor_id, measure['date'], measure['unit'], json.dumps(measure['value'])] ) for sensor_id, measure in self.measures.items()]
    cursor.close()
    db.commit()
    db.close()
    logger.info(f"DB:insert {len(self.measures)} rows")

  def history(self):
    db = sqlite3.connect('smart4l.db')
    cursor = db.cursor()
    cursor.execute('select date, data from smart4l')
    row = cursor.fetchone()
    res = []
    while row != None:
      res.append({"date": row[0], "data": json.loads(row[1])})
      row = cursor.fetchone()
    cursor.close()
    db.commit()
    db.close()
        
    return res

  def stop(self):
    pass
  def __str__(self):
    return f'Persistence: database location {self.database_file_path}'

  def __repr__(self):
    return str(self)
