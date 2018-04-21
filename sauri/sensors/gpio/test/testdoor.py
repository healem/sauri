import unittest
import logging
from common import loginit
from mock import Mock, patch
from sensors.gpio.door import Door
from sensors.gpio.states import State

class DoorTest(unittest.TestCase):

    goodData = "93 01 4b 46 7f ff 0d 10 32 : crc=32 YES\n93 01 4b 46 7f ff 0d 10 32 t=25187"
    badCrc = "93 01 4b 46 7f ff 0d 10 32 : crc=32 NO\n93 01 4b 46 7f ff 0d 10 32 t=25187"
    zeroTemp = "93 01 4b 46 7f ff 0d 10 32 : crc=32 YES\n93 01 4b 46 7f ff 0d 10 32 t=0"
    noTemp = "93 01 4b 46 7f ff 0d 10 32 : crc=32 YES\n93 01 4b 46 7f ff 0d 10 32 t="
    invalidTemp = "93 01 4b 46 7f ff 0d 10 32 : crc=32 YES\n93 01 4b 46 7f ff 0d 10 32 t=dfhg"
    empty = ""
    name = "testSensorName"
    pin = 23

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        DoorTest.logger = logging.getLogger(__name__)
            
    @patch('RPi.GPIO.input')
    def test_getStateOpen(self, gpioMock):
         gpioMock.return_value = 1
         sensor = Door(DoorTest.name, DoorTest.pin)
         self.assertEqual(sensor.getState(), State.OPEN)
         
    @patch('RPi.GPIO.input')
    def test_getStateClosed(self, gpioMock):
         gpioMock.return_value = 0
         sensor = Door(DoorTest.name, DoorTest.pin)
         self.assertEqual(sensor.getState(), State.CLOSED)