import os
import uuid
from datetime import datetime

import redis
import pika
import json
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем пароль из .env
REDIS_USER = os.getenv("REDIS_USER")
REDIS_USER_PASSWORD = os.getenv("REDIS_USER_PASSWORD")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_QUEUE = 'books_network'
DB_NUMBER = 0


class BaseClient:
    def __init__(self):
        # Подключение к Redis
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=DB_NUMBER, username=REDIS_USER, password=REDIS_USER_PASSWORD)
        # Подключение к RabbitMQ
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials, heartbeat=600))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=RABBITMQ_QUEUE)

    def model_name(self):
        return 'default'

    def send_action(self, action, data):
        """Отправляет действие в RabbitMQ."""
        message = {
            'model': self.model_name(),
            'action': action,
            'data': data
        }
        self.channel.basic_publish(exchange='',routing_key=RABBITMQ_QUEUE, body=json.dumps(message))

    def get(self, item_id):
        """Получает элемент из Redis."""
        item_data = self.redis.get(f'{self.model_name()}:{item_id}')
        if not item_data:
            raise ValueError(f"{self.model_name()} {item_id} not found")
        return json.loads(item_data)

    def create(self, data):
        """Создает новый элемент в Redis и отправляет событие в RabbitMQ."""
        item_id = data.get('id', str(uuid.uuid4()))
        data['created_at'] = datetime.now().isoformat()
        data['updated_at'] = data['created_at']
        
        self.redis.set(f'{self.model_name()}:{item_id}', json.dumps(data))
        self.send_action('create', data)
        return item_id

    def update(self, item_id, **kwargs):
        """Обновляет элемент в Redis и отправляет событие в RabbitMQ."""
        item_data = self.get(item_id)
        
        # Обновляем только переданные поля
        for key, value in kwargs.items():
            if value is not None:
                item_data[key] = value
        
        item_data['updated_at'] = datetime.now().isoformat()
        
        self.redis.set(f'{self.model_name()}:{item_id}', json.dumps(item_data))
        self.send_action('update', {'id': item_id, **kwargs})

    def delete(self, item_id):
        """Удаляет элемент из Redis и отправляет событие в RabbitMQ."""
        if not self.redis.exists(f'{self.model_name()}:{item_id}'):
            raise ValueError(f"{self.model_name()} {item_id} not found")

        self.redis.delete(f'{self.model_name()}:{item_id}')
        self.send_action('delete', {'id': item_id})

    def add_many(self, items, chunk_size=100):
        """Добавляет много элементов в Redis и отправляет событие в RabbitMQ."""
        for i in range(0, len(items), chunk_size):
            chunk = items[i:i + chunk_size]
            for item in chunk:
                item_id = item.get('id', str(uuid.uuid4()))
                item['created_at'] = datetime.now().isoformat()
                item['updated_at'] = item['created_at']
                self.redis.set(f'{self.model_name()}:{item_id}', json.dumps(item))
            self.send_action('add_many', chunk)

    def close(self):
        """Закрывает соединение с RabbitMQ."""
        self.connection.close()


class BookClient(BaseClient):
    def model_name(self):
        return 'book'
