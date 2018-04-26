import unittest
import logging
from common import loginit
from mock import Mock, patch
from sensors.gpio.door import Door
from sensors.gpio.states import State

class DoorTest(unittest.TestCase):
    name = "testSensorName"
    pin = 23

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        DoorTest.logger = logging.getLogger(__name__)
        
    @patch('RPi.GPIO.input')
    def test_getRawData(self, gpioMock):
         gpioMock.return_value = 0
         sensor = Door(DoorTest.name, DoorTest.pin)
         self.assertEqual(sensor.getRawData(), State.CLOSED)
            
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
         
    def test_notifyOnStateChangeNoCallback(self):
         sensor = Door(DoorTest.name, DoorTest.pin)
         with self.assertRaises(ValueError):
            sensor.notifyOnStateChange(None)
            
    @patch('RPi.GPIO.add_event_detect')
    @patch('RPi.GPIO.remove_event_detect')
    @patch('RPi.GPIO.input')
    def test_notifyOnStateChangeClosed(self, gpioInputMock, gpioRemoveMock, gpioAddMock):
         gpioInputMock.return_value = 0
         sensor = Door(DoorTest.name, DoorTest.pin)
         sensor.notifyOnStateChange(self.dummyCallback)
         self.assertEqual(sensor.callback, self.dummyCallback)
         
    @patch('RPi.GPIO.add_event_detect')
    @patch('RPi.GPIO.remove_event_detect')
    @patch('RPi.GPIO.input')
    def test_notifyOnStateChangeOpen(self, gpioInputMock, gpioRemoveMock, gpioAddMock):
         gpioInputMock.return_value = 1
         sensor = Door(DoorTest.name, DoorTest.pin)
         sensor.notifyOnStateChange(self.dummyCallback)
         self.assertEqual(sensor.callback, self.dummyCallback)        

    @patch('RPi.GPIO.input')
    def test_handleStateChangeNoCallback(self, gpioInputMock):
         gpioInputMock.return_value = 0
         sensor = Door(DoorTest.name, DoorTest.pin)
         sensor.callback = None
         with self.assertRaises(ValueError):
            sensor._handleStateChange(23)
            
    @patch('sensors.gpio.door.Door.notifyOnStateChange')
    @patch('RPi.GPIO.add_event_detect')
    @patch('RPi.GPIO.remove_event_detect')
    @patch('RPi.GPIO.input')
    def test_handleStateChangeSuccess(self, gpioInputMock, gpioRemoveMock, gpioAddMock, notifyMock):
         gpioInputMock.return_value = 0
         sensor = Door(DoorTest.name, DoorTest.pin)
         sensor.callback = self.dummyCallback
         sensor._handleStateChange(23)
         notifyMock.assert_called_with(self.dummyCallback)
         
    @patch('RPi.GPIO.remove_event_detect')
    def test_disableStateChangeNotification(self, gpioRemoveMock):
         sensor = Door(DoorTest.name, DoorTest.pin)
         sensor.callback = self.dummyCallback
         sensor.disableStateChangeNotification()
         self.assertEqual(sensor.callback, None)
         
    def dummyCallback(self, sensor, state):
        pass