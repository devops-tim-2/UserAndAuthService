import pika
from os import environ

params = pika.URLParameters(environ('RABBITMQ_URI'))
connection = pika.BlockingConnection(params)
channel = connection.channel()


channel.start_consuming()
channel.close()