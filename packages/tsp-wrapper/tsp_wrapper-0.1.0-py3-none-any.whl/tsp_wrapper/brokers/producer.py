from kombu import Producer
from .broker import Broker, BrokerConnectionProtocol
from enum import Enum
import logging


logger = logging.getLogger("root")

class DeliveryMode(Enum):
    NOT_PERSISTENT = 1
    PERSISTENT = 2

class ProducerKombu(Broker):
    def __init__(self, broker: BrokerConnectionProtocol):
        self.broker = broker
        self.channel = broker.channel
        self.producer = Producer(
            channel=self.channel,
            auto_declare=True,
            serializer="json")
        self.producer.declare()
        self._data = None

    def set_producer_data(self, data):
        self._data = data

    def run(self):
        self.producer.publish(
            **self._data,
            auto_declare=True,
            serializer="json",
            delivery_mode=DeliveryMode.PERSISTENT.value
            )

    def stop(self):
        logger.info("shuttings down")
        self.broker._connection.close()