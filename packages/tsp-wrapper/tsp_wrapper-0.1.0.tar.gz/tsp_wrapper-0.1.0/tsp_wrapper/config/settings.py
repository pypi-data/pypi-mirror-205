from decouple import config


BROKER_URL = config("BROKER_URL", default="amqp://guest:guest@localhost:5672/")

INBOUND_QUEUE          = config("INBOUND_QUEUE", default="inbound")
INBOUND_EXCHANGE_NAME  = config("INBOUND_EXCHANGE_NAME", default="inbound")
INBOUND_EXCHANGE_TYPE  = config("INBOUND_EXCHANGE_TYPE", default="topic") 
INBOUND_DURABLE        = config("INBOUND_DURABLE", default=True, cast=bool) 
INBOUND_ROUTING_KEY    = config("INBOUND_ROUTNG_KEY", default="inbound") 

OUTBOUND_QUEUE         = config("OUTBOUND_QUEUE", default="outbound")
OUTBOUND_EXCHANGE_NAME = config("OUTBOUND_EXCHANGE_NAME", default="outbound")
OUTBOUND_EXCHANGE_TYPE = config("OUTBOUND_EXCHANGE_TYPE", default="topic")
OUTBOUND_DURABLE       = config("OUTBOUND_DURABLE", default=True, cast=bool)
OUTBOUND_ROUTING_KEY   = config("OUTBOUND_ROUTING", default="outbound") 