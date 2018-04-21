import os.path
import time
import logging
import RPi.GPIO as gpio
from sensors.gpio.gpioSensor import GpioSensor
from sensors.gpio.types import Type

logger = logging.getLogger(__name__)

class Binary(GpioSensor):
    """Gets data from binary sensor """
    def __init__(self, name, gpioType, pin, ioMode, pullUpMode):
        """Initialize the sensor object """
        super(Binary, self).__init__(name, gpioType, pin)
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, ioMode, pull_up_down=pullUpMode)