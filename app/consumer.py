import pika
import json
import time
from app.tasks import run_container

def connect_to_rabbitmq():
    for i in range(10):  # Try to connect 10 times
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f'Connection to RabbitMQ failed, retrying in {2 ** i} seconds...')
            time.sleep(2 ** i)
    raise Exception('Failed to connect to RabbitMQ after multiple attempts')

def callback(ch, method, properties, body):
    message = json.loads(body)
    backend_host = message.get('backendHost')
    pipeline_run_step_id = message.get('pipelineRunStepId')

    if not backend_host or not pipeline_run_step_id:
        print("Invalid message received")
        return

    run_container.delay(backend_host, pipeline_run_step_id)

def start_consuming():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='pipeline-run-step', durable=True)

    channel.basic_consume(queue='pipeline-run-step', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
