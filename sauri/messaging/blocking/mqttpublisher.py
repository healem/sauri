import ssl
import logging
from messaging.blocking.mqttbase import MQTTBase

logger = logging.getLogger(__name__)

class MQTTPublisher(MQTTBase):
    """Blocking message mqtt publisher"""
    
    def __init__(self, host, port, caCertsFile, keyFile, certFile):
        """ Initialization of MQTT publisher
        
        Args:
            host (str):          FQDN or IP of broker
            port (int):          TCP port number to connect to the broker
            caCertsFile (str):   File container ca certificates
            keyFile (str):       File containing private key for client
            certFile (str):      File containing certificate for client
        """
        super(MQTTPublisher, self).__init__(host, port, caCertsFile, keyFile, certFile)
            
    def publish(self, topicName, message, exchangeName=None):
        """ Publish message to broker
        
        Args:
            topicName (str): Routing key name, such as anonymous.info
            message (str): Message to send to broker
            exchangeName (str): not needed for MQTT
            # not added yet qos (int): qos=0: message left, qos=1,2: handshake completed
            # not added yet retain (bool): keep the message on the broker as last known good
            
        """
        qos = 2
        retain = True
        
        if self.connected is False:
            self.connect()
            
        try:
            result, mid = self.client.publish(topicName, message, qos, retain)
            if result != self.client.MQTT_ERR_SUCCESS:
                logger.error("Unable to publish message: {} to topic {} on host {}".format(message, topicName, self.host))
                return
            logger.debug("Published message: {} to topic {} on host {}".format(message, topicName, self.host))
        except (ValueError):
            logger.error("Unable to publish message due to invalid topic, unset qos, or message is too long for topic: {} and message {}".format(topicName, message))
    
        
    def publishOneShot(self, topicName, message, exchangeName=None):
        """ Connect, publish message, disconnect
        
        Args:
            same as publish

        """
        self.publish(topicName, message)
        self.disconnect()