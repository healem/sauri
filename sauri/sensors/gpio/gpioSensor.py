import os.path
import logging
from sensors.sensor import Sensor
from sensors.categories import Category
from sensors.gpio.types import Type

logger = logging.getLogger(__name__)

class GpioSensor(Sensor):
    """Generic gpio sensor interface"""
    def __init__(self, name, sensorType, pin):
        super(GpioSensor, self).__init__(name, Category.GPIO, sensorType, None, pin)
        self.callback = None
        
    def getRawData(self):
        raise NotImplementedError("Abstract base class: does not implement getRawData")
    
    def getState(self):
        raise NotImplementedError("Abstract base class: does not implement getState")
    
    def notifyOnStateChange(self):
        raise NotImplementedError("Abstract base class: does not implement notifyOnStateChange")
    
    def disableStateChangeNotification(self):
        raise NotImplementedError("Abstract base class: does not implement disableStateChangeNotification")