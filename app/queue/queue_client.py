from rq import Queue
from app.core.redis_client import redis_conn

queue = Queue("default", connection=redis_conn)