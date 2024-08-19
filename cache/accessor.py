import redis
import os


def get_redis_connection() -> redis.Redis:
    return redis.Redis(host='localhost', port=6379, db=0)


def set_pomodoro_count(task_id: int, count: int) -> None:
    redis_conn = get_redis_connection()
    redis_conn.hset(f'pomodoro_count:{task_id}', 'count', count)