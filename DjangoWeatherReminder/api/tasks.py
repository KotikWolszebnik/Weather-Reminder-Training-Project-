from celery import shared_task

from .models import Subscription
from .utils import send_remind


@shared_task
def send_weather_notification(period: int):
    subscriptions = Subscription.objects.filter(notification_period=period)
    for subscription in subscriptions:
        send_remind(subscription.user, subscription.city.id)
