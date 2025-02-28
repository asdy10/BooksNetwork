import time

import requests

while True:

    t = time.time()
    # Чтение 10 случайных ключей
    for _ in range(100):
        res = requests.get('http://api-worker:8000/get')

    print('get many', time.time() - t)
    time.sleep(10)