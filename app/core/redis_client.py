import os
from redis import Redis
from rq import Queue


def get_redis_connection() -> Redis:
    """
    Returns Redis connection used by RQ.
    """
    REDIS_HOST = os.getenv("REDIS_HOST", "Host.docker.internal")
    port = int(os.environ.get("REDIS_PORT", 6379))

    return Redis(host=REDIS_HOST, port=port)


# Create queue instance

redis_conn = get_redis_connection()

queue = Queue(
    "default",
    connection=redis_conn
)