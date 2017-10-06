import os.path
import logging
from sensors.sensor import Sensor
from sensors.categories import Category

logger = logging.getLogger(__name__)

class TemperatureSensor(Sensor):
    """Generic temperature sensor interface"""
    def __init__(self, name, sensorType, path):
        super(TemperatureSensor, self).__init__(name, Category.TEMPERATURE, sensorType, path)
        
    def getRawData(self):
        raise NotImplementedError("Abstract base class: does not implement getRawData")
    
    def getTempC(self, retries):
        raise NotImplementedError("Abstract base class: does not implement getTempC")
    
    def getTempF(self, retries):
        raise NotImplementedError("Abstract base class: does not implement getTempF")