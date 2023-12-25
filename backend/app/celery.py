import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'increase-every-3-hour': {'task': 'tasks.increase_debt_task', 'schedule': timedelta(hours=3)},
}

app.conf.beat_schedule = {
    'decrease-every-morning': {'task': 'tasks.decrease_debt_task', 'schedule': crontab(hour=6, minute=30)},
}

app.conf.timezone = 'UTC'
