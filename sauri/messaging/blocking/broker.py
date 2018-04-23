import logging
from messaging.types import Type
from messaging.broker import Broker
from messaging.blocking.factory import BlockingMessagerFactory

logger = logging.getLogger(__name__)

class BlockingBroker(Broker):
    """ Generic blocking broker interface """
    def __init__(self, brokerConfig):
        super(BlockingBroker, self).__init__(brokerConfig)
        self.publisher = None
        self.subscriber = None
        
    def subscribe(self, callback, topicNames, exchangeName, queueName='', options=None):
        sub = self._getSubscriber()
        sub.subscribe(callback, topicNames, exchangeName, queueName, options)
    
    def unsubscribe(self):
        sub = self._getSubscriber()
        sub.unsubscribe()
    
    def publish(self, topicName, message, exchangeName=None):
        pub = self._getPublisher()
        pub.publish(topicName, message, exchangeName)
    
    def publishOneShot(self, topicName, message, exchangeName=None):
        pub = self._getPublisher()
        pub.publishOneShot(topicName, message, exchangeName)
        
    def disconnect(self):
        if self.publisher is not None:
            self.publisher.disconnect()
            
        if self.subscriber is not None:    
            self.subscriber.disconnect()
        
    def _getSubscriber(self):
        if self.subscriber is None:
            self.subscriber = BlockingMessagerFactory.getBlockingSubscriber(self.brokerConfig)
            
        return self.subscriber
    
    def _getPublisher(self):
        if self.publisher is None:
            self.publisher = BlockingMessagerFactory.getBlockingPublisher(self.brokerConfig)
            
        return self.publisher