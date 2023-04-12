from celery import Task


class BaseTaskWithRetry(Task):
    autoretry_for = (ConnectionError,)
    max_retries = 5
    retry_backoff = 10
    retry_backoff_max = 600
    retry_jitter = False
