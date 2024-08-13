import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Daily schedule recipe likes notification
app.conf.beat_schedule = {
    'send-daily-likes-notification': {
        'task': 'users.tasks.send_daily_likes_notification',
        'schedule': crontab(hour=5, minute=0),  # Executes daily at midnight in UTC
    },
}