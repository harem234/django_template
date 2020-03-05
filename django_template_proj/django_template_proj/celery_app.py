import logging
import os
from celery import Celery

from celery.signals import setup_logging

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      os.environ.get('DJANGO_SETTINGS_MODULE', 'django_template_proj.settings'))

app = Celery('django_template_proj')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.task_routes =  {
#     'user.tasks.*': {
#         'queue': 'mail',
#         # 'routing_key': 'mail',
#         # 'exchange': 'mail',
#     }
# }
# Load task modules from all registered Django app configs.
# Automatic naming and relative imports
#   from project.myapp.tasks import mytask # << GOOD task must imported in this format
#   (the they are imported in INSTALLED_APPS = ['project.myapp'])
app.autodiscover_tasks()


# app.conf.include = ['user.tasks']

# Logging #setup_logging.connect
@setup_logging.connect
def on_celery_setup_logging(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)

