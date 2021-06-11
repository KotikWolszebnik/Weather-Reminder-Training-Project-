import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoWeatherReminder.settings')

app = Celery('DjangoWeatherReminder')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


def generate_shedule() -> dict:
    shedule = dict()
    for period in [1, 3, 6, 12, 24]:
        shedule[f'run-every {period}'] = dict(
            task='tasks.send_weather_notification',
            schedule=crontab(hour=f'*/{period}'),
            kwargs=dict(period=period),
        )
    return shedule


app.conf.beat_schedule = generate_shedule()
