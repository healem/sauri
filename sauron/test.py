from common.config import Config
from common import loginit

loginit.initTestLogging()

cfg = Config("cfg/home.yaml")

for sensor in cfg.sensors:
    print("Name: {}".format(sensor['name']))

