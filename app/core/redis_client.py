import os
from redis import Redis

REDIS_HOST = os.getenv("REDIS_HOST", "Host.docker.internal")

redis_conn = Redis(host=REDIS_HOST, port=6379)

def check_redis():
    try:
        redis_conn.ping()
        return True
    except Exception:
        return False