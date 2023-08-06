import time
import socket
from kombu import Consumer
from enum import Enum
from .broker import Broker, BrokerConnectionProtocol
import logging

logger = logging.getLogger("root")

class DeliveryMode(Enum):
    NOT_PERSISTENT = 1
    PERSISTENT = 2

class ConsumerKombu(Broker):
    def __init__(self, broker: BrokerConnectionProtocol):
        self.broker = broker
        self.producer = None 
        self.channel = broker.channel
        self.message_service = None
        self.consumer =  Consumer(
            broker._connection,
            queues=broker.queues,
            auto_declare=True,
            callbacks=[self.handle_message],
            accept=["json"])

    def run(self):
        not_done = True
        time_to_wait = 0.1
        logger.info("Initializa Consumer")
        while not_done:
            not_done = True
            try:
                self.consumer.consume()
                self.broker._connection.drain_events(
                    timeout=time_to_wait)
                success = True
            except socket.timeout as t:
                self.broker._connection.heartbeat_check()
                time.sleep(0.1)

    def stop(self):
        logger.info("shutting down")
        self.broker._connection.close()

    def handle_message(self,
        body,
        message):
        """handle_message
        :param body: contents of the message
        :param message: message object
        """
        logger.info(f"callback received msg routing_key={message.delivery_info['routing_key']} ")

        if self.message_service:
            self.message_service(body, self.producer)
        message.ack()