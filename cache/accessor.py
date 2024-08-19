import redis
import os

from settings import Settings


def get_redis_connection() -> redis.Redis:
    settings = Settings()
    return redis.Redis(host=settings.CACHE_HOST, port=settings.CACHE_PORT, db=settings.CACHE_DB)


def set_pomodoro_count(task_id: int, count: int) -> None:
    redis_conn = get_redis_connection()
    redis_conn.hset(f'pomodoro_count:{task_id}', 'count', count)