from rq import Worker, Queue
from app.core.redis_client import redis_conn

if __name__ == "__main__":
    worker = Worker([Queue("default", connection=redis_conn)])
    worker.work()