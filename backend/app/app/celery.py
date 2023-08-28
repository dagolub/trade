import os
from celery import Celery  # type: ignore

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery = Celery("tasks", broker=redis_url, backend=redis_url)
