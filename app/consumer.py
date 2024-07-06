import json
import pika
import docker
import time

def process_message(message):
    backend_host = message.get('backend_host')
    pipeline_run_step_id = message.get('pipelineRunStepId')
    env_vars = {
        'BACKEND_HOST': backend_host,
        'PIPELINE_RUN_STEP_ID': str(pipeline_run_step_id)
    }
    launch_container(env_vars)

def launch_container(env_vars):
    client = docker.from_env()
    #TODO change image name
    image_name = 'python:3.9-slim'
    container = client.containers.run(
        image_name,
        detach=True,
        environment=env_vars
    )
    print(f"Container {container.id} started with environment variables {env_vars}")

def start_consuming():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            break
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ to be ready...")
            time.sleep(5)

    channel = connection.channel()
    channel.queue_declare(queue='pipeline-run-step', durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        process_message(message)

    channel.basic_consume(queue='pipeline-run-step', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()