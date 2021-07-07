# -*- coding: utf-8 -*-

from random import randint,choice

class SensorMock():
	def __init__(self, id=None) -> None:
		self.id_sensor = id

	def measure(self) -> dict:
		sensors_mock_measures = [
			{'unit': '°C', 'value': randint(150,320)/10}
			,{'unit': '%', 'value': randint(200,800)/10}
			,{'unit': 'cm', 'value': randint(1,250)}
		]
		return choice(sensors_mock_measures)

	def stop(self) -> None:
		pass

	def __str__(self):
		return f'Sensor:{self.id_sensor}'

	def __repr__(self):
		return str(self)


class SensorMockJson():
	def __init__(self, id=None) -> None:
		self.id_sensor = id

	def measure(self) -> dict:
		sensors_mock_json_measures = [
			{'unit':'°', 'value':{'latitude':randint(-90000,90000)/1000,'longitude':randint(-180000,180000)/1000}}
			,{'unit': '°', 'value':{'x':randint(0,1800)/10,'y':randint(0,1800)/10,'z':randint(0,1800)/10}}
		]
		return choice(sensors_mock_json_measures)

	def stop(self) -> None:
		pass

	def __str__(self):
		return f'Sensor:{self.id_sensor}'

	def __repr__(self):
		return str(self)