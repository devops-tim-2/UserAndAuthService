from broker.consumer import AdminConsumer
import pika
from os import environ

params = pika.URLParameters(environ.get('RABBITMQ_URI'))
connection = pika.BlockingConnection(params)
channel = connection.channel()

admin_queue = AdminConsumer(channel)

print(f'Started admin_queue: {type(admin_queue)}')

channel.start_consuming()
channel.close()