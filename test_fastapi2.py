import time

import requests

while True:

    t = time.time()
    # Чтение 10 случайных ключей
    res = requests.get('http://api-worker:8000/get_many')
    print('get many1', time.time() - t)
    t = time.time()
    for _ in range(10):
        res = requests.get('http://api-worker:8000/get_many')

    print('get many2', time.time() - t)
    time.sleep(10)