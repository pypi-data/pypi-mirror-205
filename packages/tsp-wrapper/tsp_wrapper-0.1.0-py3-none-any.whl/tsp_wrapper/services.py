from tsp_wrapper.brokers.broker import BrokerConnectionKombu, Broker
from tsp_wrapper.brokers.builder import BrokerQueueBuilder, BrokerType
from kombu import Exchange, Queue
from tsp_wrapper.config.settings import (BROKER_URL, INBOUND_DURABLE, INBOUND_EXCHANGE_NAME,
                                  INBOUND_EXCHANGE_TYPE, INBOUND_QUEUE, INBOUND_ROUTING_KEY,
                                  OUTBOUND_DURABLE, OUTBOUND_EXCHANGE_NAME, OUTBOUND_QUEUE,
                                  OUTBOUND_EXCHANGE_TYPE, OUTBOUND_ROUTING_KEY)
 

def pipeline_broker(broker_connection: BrokerConnectionKombu, exchange_name: str = INBOUND_EXCHANGE_NAME,
                    routing_key: str = INBOUND_ROUTING_KEY) -> None:
    producer_data = { "body": "NOthing", "exchange_name": exchange_name, "routing_key": routing_key}
    exchange = Exchange(
                INBOUND_EXCHANGE_NAME,
                type=INBOUND_EXCHANGE_TYPE,
                durable=INBOUND_DURABLE)
    broker = BrokerQueueBuilder(broker_connection=broker_connection)
    return broker\
        .works_as_a(broker_type=BrokerType.CONSUMER.value)\
        .with_exchange(exchange)\
        .with_queue([Queue(
            INBOUND_QUEUE,
            exchange,
            routing_key=INBOUND_ROUTING_KEY,
            durable=INBOUND_DURABLE),])\
        .get_broker(producer_data=producer_data)

def outbound_queue_producer(broker_connection: BrokerConnectionKombu, exchange_name: str = OUTBOUND_EXCHANGE_NAME,
                            routing_key: str = OUTBOUND_ROUTING_KEY) -> Broker:

    producer_data = { "body": None, "exchange_name": exchange_name, "routing_key": routing_key}
    exchange = Exchange(
                exchange_name,
                type=OUTBOUND_EXCHANGE_TYPE,
                durable=OUTBOUND_DURABLE)
    broker = BrokerQueueBuilder(broker_connection=broker_connection)
    return broker\
        .works_as_a(broker_type=BrokerType.PRODUCER.value)\
        .with_exchange(exchange)\
        .with_queue([Queue(
            OUTBOUND_QUEUE,
            exchange,
            routing_key=OUTBOUND_ROUTING_KEY,
            durable=OUTBOUND_DURABLE),])\
        .get_broker(producer_data=producer_data)

def inbound_queue_producer(problem: list[dict], exchange_name: str = INBOUND_EXCHANGE_NAME, 
                           routing_key: str = INBOUND_ROUTING_KEY, url: str = BROKER_URL) -> None:

    with BrokerConnectionKombu(url=url) as broker_connection: 
        producer_data = { "body": problem, "exchange_name": exchange_name, "routing_key": routing_key}
        exchange = Exchange(
                    exchange_name,
                    type=INBOUND_EXCHANGE_TYPE,
                    durable=INBOUND_DURABLE)
        broker = BrokerQueueBuilder(broker_connection=broker_connection)
        broker_setup = broker\
            .works_as_a(broker_type=BrokerType.PRODUCER.value)\
            .with_exchange(exchange)\
            .with_queue([Queue(
                INBOUND_QUEUE,
                exchange,
                routing_key=INBOUND_ROUTING_KEY,
                durable=INBOUND_DURABLE),])\
            .run(producer_data=producer_data)

def outbound_queue_concumer(exchange_name: str = OUTBOUND_EXCHANGE_NAME, routing_key: str = OUTBOUND_ROUTING_KEY,
                           url: str = BROKER_URL) -> None:

    with BrokerConnectionKombu(url=url) as broker_connection: 
        producer_data = { "body": "", "exchange_name": exchange_name, "routing_key": routing_key}
        exchange = Exchange(
                    exchange_name,
                    type=OUTBOUND_EXCHANGE_TYPE,
                    durable=OUTBOUND_EXCHANGE_TYPE)
        broker = BrokerQueueBuilder(broker_connection=broker_connection)
        broker = broker\
            .works_as_a(broker_type=BrokerType.CONSUMER.value)\
            .with_exchange(exchange)\
            .with_queue([Queue(
                OUTBOUND_QUEUE,
                exchange,
                routing_key=OUTBOUND_ROUTING_KEY,
                durable=OUTBOUND_EXCHANGE_TYPE),])\
            .get_broker(producer_data=producer_data)
        broker.message_service = None
        broker.run()