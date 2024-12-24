import redis


REDIS_FLAG_TRADE_RUNIT = "REDIS_FLAG_TRADE_RUNIT"
REDIS_FLAG_CURRENT_LOGGING_EVENTS_ENABLED = "REDIS_FLAG_CURRENT_LOGGING_EVENTS_ENABLED"


# Redis configuration
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)    