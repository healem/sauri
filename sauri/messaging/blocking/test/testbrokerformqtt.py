import unittest
import logging
from common import loginit
from mock import Mock, patch, mock_open
from messaging.blocking.broker import BlockingBroker
from messaging.blocking.mqttpublisher import MQTTPublisher

class BlockingBrokerMQTTTest(unittest.TestCase):
    
    config = {'name':'minix', 'protocol':'mqtt', 'type':'blocking', 'address':'127.0.0.1', 'port':9999,
              'ca_certs':'/home/ca.pem', 'key_file':'/home/key.pem', 'cert_file':'/home/cert.pem'}
    
    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        BlockingBrokerMQTTTest.logger = logging.getLogger(__name__)
        
    @patch('os.path.isfile')
    def test_goodInit(self, osMock):
        cfg = BlockingBrokerMQTTTest.config
        osMock.return_value = True
        
        broker = BlockingBroker(cfg)
        self.assertEqual(broker.brokerName, cfg['name'])
        self.assertEqual(broker.protocol, cfg['protocol'])
        self.assertEqual(broker.brokerType, cfg['type'])
        self.assertEqual(broker.host, cfg['address'])
        self.assertEqual(broker.port, cfg['port'])
        self.assertEqual(broker.caCertsFile, cfg['ca_certs'])
        self.assertEqual(broker.keyFile, cfg['key_file'])
        self.assertEqual(broker.certFile, cfg['cert_file'])
        self.assertEqual(broker.brokerConfig, cfg)
            
    @patch('os.path.isfile')
    def test_badCertsPath(self, osMock):
        cfg = BlockingBrokerMQTTTest.config
        osMock.return_value = False
        
        with self.assertRaises(IOError):
            b = BlockingBroker(cfg)
        
    @patch('messaging.blocking.mqttbase.MQTT.Client')
    def test_goodPublish(self, mqttMock):
        self.broker = self._getBroker()
        
        topic1 = "topic.one"
        msg = "Test message"
        
        mqttMock.return_value.publish.return_value = (0, 0)
        self.broker.publish(topic1, msg)
        BlockingBrokerMQTTTest.logger.info("MQTT calls: {}".format(mqttMock.mock_calls))

        # Make sure the channel and connection are NOT closed after publishing a message
        mqttMock.return_value.publish.assert_called_with(topic1, msg, 2, True)
        assert not mqttMock.disconnect.called
        
    @patch('messaging.blocking.mqttbase.MQTT.Client')
    def test_goodPublishRetry(self, mqttMock):
        self.broker = self._getBroker()
        
        topic1 = "topic.one"
        msg = "Test message"
        
        mqttMock.return_value.publish.side_effect = iter([(self.broker.client.MQTT_ERR_NO_CONN, 0), (0,0)])
        self.broker.publish(topic1, msg)
        BlockingBrokerMQTTTest.logger.info("MQTT calls: {}".format(mqttMock.mock_calls))

        # Make sure the channel and connection are NOT closed after publishing a message
        mqttMock.return_value.publish.assert_called_with(topic1, msg, 2, True)
        assert not mqttMock.disconnect.called
        
    @patch('messaging.blocking.mqttbase.MQTT.Client')
    def test_goodPublishOneShot(self, mqttMock):
        self.broker = self._getBroker()
        
        topic1 = "topic.one"
        msg = "Test message"

        self.broker.publishOneShot(topic1, msg)
        BlockingBrokerMQTTTest.logger.info("MQTT calls: {}".format(mqttMock.mock_calls))

        # Make sure the channel and connection are cleaned up after calling one shot
        mqttMock.return_value.publish.assert_called_with(topic1, msg, 2, True)
        assert mqttMock.return_value.disconnect.called
        
    @patch('os.path.isfile')
    def _getBroker(self, osMock):
        osMock.return_value = True
        return BlockingBroker(BlockingBrokerMQTTTest.config)
    
    def testCallback(self):
        return True
    
    def exceptOnce(self, exception, throwBool):
        if throwBool is True:
            return exception
        
        
# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()
        
    