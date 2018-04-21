import os.path
import time
import logging
import RPi.GPIO as gpio
from sensors.gpio.gpioSensor import GpioSensor
from sensors.gpio.binary import Binary
from sensors.gpio.types import Type
from sensors.gpio.states import State

logger = logging.getLogger(__name__)

class Door(Binary):
    """Gets data from door sensor """
    def __init__(self, name, pin):
        """Initialize the sensor object """
        super(Door, self).__init__(name, Type.DOOR, pin, gpio.IN, gpio.PUD_UP)
        
    def getRawData(self):
        return self.getState()
        
    def getState(self):
        if gpio.input(self.pin):
            return State.OPEN
        else:
            return State.CLOSED
        
    def notifyOnStateChange(self, callback):
        if callback == None:
            logger.error("Invalid callback registered for notifyOnStateChange for sensor {}".format(self.name))
            raise ValueError("Cannot set callback to None on notifyOnStateChange for sensor {}".format(self.name))
        
        logger.info("Sensor {} will notify when its state changes".format(self.name))
        self.callback = callback
        gpio.remote_event_detect(self.pin)
        if self.getState() == State.Open:
            gpio.add_event_detect(self.pin, gpio.FALLING, callback=self.handleStateChange, bouncetime=300)
        else:
            gpio.add_event_detect(self.pin, gpio.RISING, callback=self.handleStateChange, bouncetime=300)
        
    def handleStateChange(self, pin):
        state = self.getState()
        logger.debug("Sensor {} observed a state change to {}".format(self.name, state))
        if self.callback == None:
            logger.error("Got notified of state change on sensor {}, but no callback is registered".format(self.name))
            
        self.callback(state)
        
        # re-register the callback
        self.notifyOnStateChange(self.callback)
        
    def disableStateChangeNotification(self):
        logger.info("Sensor {} will no longer notify when its state changes".format(self.name))
        gpio.remote_event_detect(self.pin)
        self.callback = None
            