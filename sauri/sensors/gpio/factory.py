from sensors.gpio.types import Type
from sensors.gpio.binary import Binary
from sensors.gpio.door import Door
import logging

logger = logging.getLogger(__name__)

class GpioSensorFactory(object):
    """ Factory to create GpioSensor objects """
    def getGpioSensor(sensorConfig):
        """ Initialization of factory
        
        Args:
            sensorConfig (dict): subsection of configuration pertinent to this sensor
            
        Returns:
            GpioSensor : GpioSensor object
        """
        if (sensorConfig['type'] == Type.DOOR):
            sensor = Door(sensorConfig['name'], sensorConfig['pin'])
            return sensor
        else:
            logger.error("GpioSensor type {} not found".format(sensorConfig['type']))
            raise ValueError("GpioSensor type {} not found".format(sensorConfig['type']))
    getGpioSensor = staticmethod(getGpioSensor)