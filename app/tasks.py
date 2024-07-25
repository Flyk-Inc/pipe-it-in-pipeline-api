from . import celery_app
import docker
from dotenv import load_dotenv
import os
import time
import requests

load_dotenv()

@celery_app.task
def run_container(backend_host, pipeline_run_step_id):
    image_name = os.getenv('DOCKER_IMAGE_NAME')
    timeout_minutes = int(os.getenv('TIMEOUT_MINUTES', 5))

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

    start_time = time.time()

    while time.time() - start_time < timeout_minutes * 60:
        container.reload()
        if container.status == 'exited':
            print(f'Container {container.short_id} finished')
            print(f'Logs:\n{container.logs().decode("utf-8")}')
            container.remove(force=True)
            print(f'Container {container.short_id} deleted')
            return

        time.sleep(10)

    # Timeout handling
    print(f'Timeout reached for container {container.short_id}')
    print(f'Logs:\n{container.logs().decode("utf-8")}')
    container.remove(force=True)
    print(f'Container {container.short_id} deleted after timeout')

    # Notify backend about the timeout
    requests.patch(
        f'{backend_host}/pipeline/step/{pipeline_run_step_id}/end',
        json={
            'stdout': '',
            'stderr': 'Timeout, the code never ended',
            'isError': True,
            'outputFileId': None
        }
    )
    print(f'Notified backend of timeout for pipeline run step {pipeline_run_step_id}')
