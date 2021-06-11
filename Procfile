web: gunicorn --pythonpath DjangoWeatherReminder DjangoWeatherReminder.wsgi
worker: celery --workdir DjangoWeatherReminder -A DjangoWeatherReminder worker