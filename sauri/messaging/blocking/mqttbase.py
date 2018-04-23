import ssl
import paho.mqtt.client as MQTT
import logging

logger = logging.getLogger(__name__)

class MQTTBase(object):
    """Blocking message mqtt broker"""
    
    def __init__(self, host, port, caCertsFile, keyFile, certFile):
        """ Initialization of MQTT broker
        
        Args:
            host (str):          FQDN or IP of broker
            port (int):          TCP port number to connect to the broker
            caCertsFile (str):   File container ca certificates
            keyFile (str):       File containing private key for client
            certFile (str):      File containing certificate for client
        """
        self.host = host
        self.port = port
        self.caCertsFile = caCertsFile
        self.keyFile = keyFile
        self.certFile = certFile
        self.client = MQTT.Client()
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        self.client.on_log = self._on_log
        self.client.tls_set(ca_certs=self.caCertsFile, certfile=self.certFile, keyfile=self.keyFile, cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.connected = False
        
    def connect(self):
        """ Connect to broker """
        logger.debug("Connecting to MQTT broker {}:{}".format(self.host, self.port))
        self.client.connect(self.host, port=self.port, keepalive=60, bind_address="")
        logger.debug("Connected to MQTT broker {}:{}".format(self.host, self.port))
        
    def reconnect(self):
        """ Check if the channel and connection are open, if not then reconnect"""
        logger.debug("Reconnecting to MQTT broker {}:{}".format(self.host, self.port))
        self.client.reconnect()
        
    def disconnect(self):
        """ Disconnect from broker """
        self.client.disconnect()
        logger.debug("Disconnected from MQTT broker {}:{}".format(self.host, self.port))
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.debug("Connection successful to {}".format(self.host))
            self.connected = True
        elif rc == 1:
            logger.error("Connection to broker {} failed: Connection refused - incorrect protocol version".format(self.host))
        elif rc == 2:
            logger.error("Connection to broker {} failed: Connection refused - invalid client identifier".format(self.host))
        elif rc == 3:
            logger.error("Connection to broker {} failed: Connection refused - server unavailable".format(self.host))
        elif rc == 4:
            logger.error("Connection to broker {} failed: Connection refused - bad username or password".format(self.host))
        elif rc == 5:
            logger.error("Connection to broker {} failed: Connection refused - not authorized".format(self.host))
        else:
            logger.error("Connection to broker {} failed for unknown reason".format(self.host))
            
    def _on_disconnect(client, userdata, rc):
        logger.debug("Disconnection successful to {}".format(self.host))
        self.connected = False

    def _on_publish(self, client, obj, mid):
        logger.debug("Message published, mid: {}".format(mid))
        
    def _on_log(self, client, userdata, level, buf):
        if level == MQTT_LOG_ERR:
            logger.error("MQTT Client: {}".format(buf))
        elif level == MQTT_LOG_WARNING:
            logger.warn("MQTT Client: {}".format(buf))
        elif level == MQTT_LOG_NOTICE:
            logger.info("MQTT Client: {}".format(buf))
        elif level == MQTT_LOG_INFO:
            logger.info("MQTT Client: {}".format(buf))
        elif level == MQTT_LOG_DEBUG:
            logger.debug("MQTT Client: {}".format(buf))

        