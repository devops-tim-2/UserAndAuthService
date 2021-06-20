import pika, json
from os import environ

params = pika.URLParameters(environ.get('RABBITMQ_URI'))

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    print(f"########{method}#######")
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='user', body=json.dumps(body), properties=properties)