# app/tasks.py
from . import celery_app
import docker


@celery_app.task
def run_container():
    client = docker.from_env()
    container = client.containers.run(
        #TODO replace image name
        "python:3.9-slim",  # Remplacer par le nom réel de votre image
        command="sleep 10",
        detach=True
    )
    print(f'Container {container.short_id} started')

    # Attendre que le conteneur se termine
    container.wait()
    print(f'Container {container.short_id} finished')
