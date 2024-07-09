broker_url = 'pyamqp://guest@rabbitmq//'
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

worker_concurrency = 5  # Limiter le nombre de tâches simultanées à 5
broker_connection_retry_on_startup = True  # Réessayer de se connecter au démarrage

# Limite combien de tâches un worker peut pré-récupérer avant de les traiter
worker_prefetch_multiplier = 1