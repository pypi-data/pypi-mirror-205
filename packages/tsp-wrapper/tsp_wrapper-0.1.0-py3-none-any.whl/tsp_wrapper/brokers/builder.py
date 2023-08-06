from .producer import ProducerKombu
from .consumer import ConsumerKombu
from .broker import BrokerConnectionProtocol

from tsp_wrapper.tsp import run_tsp
from kombu import Exchange
from enum import Enum

from dataclasses import dataclass


class BrokerType(Enum):
    PRODUCER = "producer"
    CONSUMER = "consumer"

@dataclass
class BrokerSetup:
    broker: BrokerConnectionProtocol
    broker_type: BrokerType = BrokerType.CONSUMER.value
    exchange: Exchange|None = None
    queues: list|None = None
 
class BrokerBuilder:
    def __init__(self, broker_connection: BrokerConnectionProtocol) -> None:
        self.broker_setup = BrokerSetup(
            broker=broker_connection
        )

    def build(self):
        return self.broker_setup
    
    def get_broker(self, producer_data: dict):
        broker_setup = self.broker_setup
        broker_setup.broker.get_channel()
        broker_setup.broker.bind_queues(broker_setup.queues)

        if broker_setup.broker_type == BrokerType.PRODUCER.value:
            broker = ProducerKombu(broker=broker_setup.broker)
            broker.set_producer_data(data=producer_data)
        else:
            broker = ConsumerKombu(broker=broker_setup.broker)
            broker.message_service = run_tsp
        return broker


    def run(self, producer_data: dict):
        broker = self.get_broker(producer_data=producer_data)
        broker.run()

class BrokerTypeBuilder(BrokerBuilder):
    def works_as_a(self, broker_type):
        self.broker_setup.broker_type = broker_type
        return self

class BrokerExchangeBuilder(BrokerTypeBuilder):
    def with_exchange(self, exchange):
        self.broker_setup.exchange = exchange
        return self
        
class BrokerQueueBuilder(BrokerExchangeBuilder):
    def with_queue(self, queues):
        self.broker_setup.queues = queues
        return self