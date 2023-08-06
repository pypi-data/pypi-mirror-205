from kombu import Connection
from abc import ABC, abstractmethod
from typing import Protocol
import logging


logger = logging.getLogger("root")

class Broker(ABC):
    @abstractmethod
    def run(self):
        """ running the broker"""

class BrokerConnectionProtocol(Protocol):
    def connect(self):
        """ Method that connect to the broker"""
        raise NotImplementedError
 
    def disconnect(self):
        """Disconnect broker"""
        raise NotImplementedError

class BrokerConnectionKombu:
    def __init__(self, *, url:str, heartbeat:int = 60, transport_options:dict = {}, queues:list = []) -> None:
        self._url = url
        self.queues = queues
        self.heartbeat = heartbeat
        self.transport_options = transport_options
        self._connection = None
        self.channel = None

    def connect(self):
        self._connection = Connection(
            self._url,
            heartbeat=self.heartbeat,
            transport_options=self.transport_options)

    def disconnect(self):
        self._connection.close()
 
    def bind_queues(self, queues):
        self.queues = queues
        for qidx, queue_obj in enumerate(self.queues):
            try:
                queue_name = queue_obj.name
                durable = queue_obj.durable
                logger.info(f"binding queue={qidx} queue={queue_name}")
                queue_obj.maybe_bind(self._connection)
                queue_obj.declare()
            except Exception as e:
                logger.warning(f"failed creating queue={qidx} queue_declare queue={queue_name} hit ex={e}")
   
    def get_channel(self):
        self.channel = self._connection.channel()

    def __enter__(self):
        self.connect()
        logger.info(f"Broker Connected to {self._connection}")
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()
        logger.info("Disconected form broker")