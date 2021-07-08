import json
from service import user_service

class AdminConsumer:
    def __init__(self, channel):
        self.exchange_name = 'admin'
        self.channel = channel
        channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        q = channel.queue_declare(queue='')
        channel.queue_bind(exchange=self.exchange_name, queue=q.method.queue)
        channel.basic_consume(queue=q.method.queue, on_message_callback=self.on_message, auto_ack=True)

    def on_message(self, ch, method, properties, body):
        try:
            data = json.loads(body)

            if properties.content_type == 'agent.request.approve': 
                user_service.approve(data['agent_id'])
            elif properties.content_type == 'agent.request.reject': 
                user_service.reject(data['agent_id'])
            elif properties.content_type == 'user.ban': 
                user_service.delete(data['id'])
        except Exception:
            # don't crash
            pass
