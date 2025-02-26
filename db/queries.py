import os

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

    def update_user(self, user_id, name=None, email=None):
        """Обновляет пользователя в Redis и отправляет событие в RabbitMQ."""
        user_data = self.redis.get(f'user:{user_id}')
        if not user_data:
            raise ValueError(f"User {user_id} not found")

        user_data = json.loads(user_data)
        if name:
            user_data['name'] = name
        if email:
            user_data['email'] = email

        # Обновляем в Redis
        self.redis.set(f'user:{user_id}', json.dumps(user_data))

        # Отправляем событие в RabbitMQ
        self.send_action('update_user', {'id': user_id, 'name': name, 'email': email})

    def add_many(self, users, chunk_size=100):
        """Добавляет много пользователей в Redis и отправляет событие в RabbitMQ."""
        for i in range(0, len(users), chunk_size):
            chunk = users[i:i + chunk_size]
            for user in chunk:
                self.redis.set(f'user:{user["id"]}', json.dumps(user))
            self.send_action('add_many', chunk)

    def close(self):
        """Закрывает соединение с RabbitMQ."""
        self.connection.close()