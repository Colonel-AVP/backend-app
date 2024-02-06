import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

# Using a string here means the worker doesn't
# have to serialize the configuration object to
# child processes. - namespace='CELERY' means all
# celery-related configuration keys should
# have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Set broker_connection_retry_on_startup within the CELERY_ namespace
app.conf.CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
