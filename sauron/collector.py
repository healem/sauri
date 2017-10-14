from common.config import Config
from common import loginit
from sensors.factory import SensorFactory
from sensors.sensor import Sensor
from sensors.temperature.temperatureSensor import TemperatureSensor

loginit.initLogging()

cfg = Config("cfg/home.yaml")
for sensorCfg in cfg.sensors:
    sensor = SensorFactory(sensorCfg)
    reading = sensor.getData()
    print("Sensor {} has temp of {}".format(sensor.name, reading))