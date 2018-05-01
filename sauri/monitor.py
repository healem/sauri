#!/usr/bin/python
import logging
from common.config import Config
from common import loginit
import time
from sensors.factory import SensorFactory
from sensors.sensor import Sensor
from sensors.gpio.states import State
from sensors.gpio.gpioSensor import GpioSensor
from messaging.broker import Broker
from messaging.factory import BrokerFactory
import argparse

loginit.initLogging()
logger = logging.getLogger()

exchange = "sauri"
sensors =[]
brokers = []

def parseArgs():
    parser = argparse.ArgumentParser(description='Simple sensor monitor')
    parser.add_argument('-c', '--configFile', help='Full path to config file', required=True)
    parser.add_argument('-i', '--interval', type=int, default=30, help='Time between sensor collections in seconds')
    args = parser.parse_args()
    return args

def sensorChanged(sensor, state):
    logger.debug("Sensor {} changed state to {}".format(sensor.sensorName, state))
    topic = "hass/{}/{}".format(sensor.sensorType, sensor.sensorName)
    for broker in brokers:
        broker.publishOneShot(topic, state)

def initialize(cfg):
    for brokerConfig in cfg.brokers:
        broker = BrokerFactory.getBroker(brokerConfig)
        brokers.append(broker)
        
    for sensorCfg in cfg.sensors:
        sensor = SensorFactory.getSensor(sensorCfg)
        sensor.notifyOnStateChange(sensorChanged)
        sensors.append(sensor)
        
        ## Publish initial state
        topic = "hass/{}/{}".format(sensor.sensorType, sensor.sensorName)
        state = sensor.getState()
        for broker in brokers:
            broker.publishOneShot(topic, state)
            
if (__name__ == '__main__'):
    args = parseArgs()
    cfg = Config(args.configFile)
    initialize(cfg)
    while True:
        time.sleep(3000)