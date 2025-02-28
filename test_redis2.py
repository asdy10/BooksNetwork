import os
import json
import time
import random
import redis
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
REDIS_USER = os.getenv("REDIS_USER")
REDIS_USER_PASSWORD = os.getenv("REDIS_USER_PASSWORD")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
INTERVAL = int(os.getenv('WORKER_INTERVAL', 10))  # 60 seconds by default


def redis_operations():
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=1,
        username=REDIS_USER,
        password=REDIS_USER_PASSWORD,
        decode_responses=True
    )

    while True:
        # try:
        # Чтение специального ключа
        t = time.time()
        special_data = r.get("special_key")
        print(f"get", time.time() - t)
        t = time.time()
        # Обновление специального ключа
        new_data = {
            "timestamp": datetime.now().isoformat(),
            "value": random.randint(0, 1000)
        }
        r.set("special_key", json.dumps(new_data))
        print('set1', time.time() - t)
        t = time.time()
        # Чтение 10 случайных ключей
        for _ in range(100):
            key = f"key_{random.randint(0, 9999)}"
            data = r.get(key)


        print('get many', time.time() - t)
        t = time.time()
        keys = [f"key_{random.randint(0, 9999)}" for i in range(10000)]
        data = r.mget(keys)
        print('get many2', time.time() - t)
        time.sleep(INTERVAL)
        # except redis.RedisError as e:
        #     print(f"Redis error: {e}")
        #     time.sleep(5)
        # except Exception as e:
        #     print(f"General error: {e}")
        #     time.sleep(5)


if __name__ == "__main__":
    print('start')
    redis_operations()
