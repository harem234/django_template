import os
from celery import Celery

# print("#" * 100)
# print(os.environ.get('DJANGO_SETTINGS_MODULE', 'django_template_proj.settings'))
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'django_template_proj.settings'))

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
app.autodiscover_tasks()
