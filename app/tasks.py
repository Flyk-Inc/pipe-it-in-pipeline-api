# app/tasks.py
from . import celery_app
import docker
from dotenv import load_dotenv
import os

load_dotenv()

@celery_app.task
def run_container(backend_host, pipeline_run_step_id):
    image_name = os.getenv('DOCKER_IMAGE_NAME')

    if not image_name:
        raise ValueError("DOCKER_IMAGE_NAME not found in environment variables")

    client = docker.from_env()
    container = client.containers.run(
        image_name,
        detach=True,
        environment={
            'BACKEND_URL': backend_host,
            'PIPELINE_RUN_STEP_ID': pipeline_run_step_id
        }
    )
    print(f'Container {container.short_id} started')

    container.wait()
    print(f'Container {container.short_id} finished')
