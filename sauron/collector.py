from common.config import Config
from common import loginit
from sensors.factory import SensorFactory
from sensors.sensor import Sensor

loginit.initLogging()

cfg = Config("cfg/home.yaml")