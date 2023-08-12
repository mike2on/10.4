import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'weekly_notifications': {
        'task': 'NewsPortal.tasks.weekly_notifications_task',
        'schedule': crontab(),
    },
}

app.autodiscover_tasks()
