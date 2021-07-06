# -*- coding: utf-8 -*-

from random import randint

class SensorMock():
	def __init__(self, id=None) -> None:
		self.id_sensor = id

	def measure(self) -> float:
		return randint(150,320)/10

	def stop(self) -> None:
		pass

	def __str__(self):
		return f'Sensor:{self.id_sensor}'

	def __repr__(self):
		return str(self)