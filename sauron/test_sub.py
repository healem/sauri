from common.config import Config
from common import loginit
from messaging.blocking.subscriber import AMQPSubscriber as Sub

loginit.initTestLogging()

cfg = Config("cfg/home.yaml")
exchange = "Test"
topic = "test.topic"
topics = [topic]

def messagePrinter(channel, method, props, body):
    print("Message received: {}:{}".format(method.routing_key,body))

for broker in cfg.brokers:
    addr = broker['address']
    port = broker['port']
    sslpw = broker['ssl_pass']
    cacert = broker['ca_certs']
    keyFile = broker['key_file']
    certFile = broker['cert_file']
    Sub = Sub(addr, port, cacert, keyFile, certFile)
    Sub.subscribe(messagePrinter, topics, exchange)