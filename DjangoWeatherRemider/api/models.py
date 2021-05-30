from django.db.models import (CASCADE, CharField, ForeignKey, IntegerField,
                              Model)
from django.contrib.auth.models import User
# Create your models here.


class Subscription(Model):
    NOTIFICATION_PERIODS = [
        (1, '1'), (3, '3'), (6, '6'), (12, '12'), (24, '24'),
    ]
    user = ForeignKey(
        User, on_delete=CASCADE, related_name='subscriptions',
    )
    city = ForeignKey('City', on_delete=CASCADE)
    notification_period = IntegerField(choices=NOTIFICATION_PERIODS)


class City(Model):
    id = IntegerField(primary_key=True, unique=True)
    name = CharField(max_length=85)
    state_code = CharField(max_length=9, null=True)
    country = CharField(max_length=100, null=True)
    country_code = CharField(max_length=3, null=True)

    def __str__(self):
        return f'< City : {self.name} >'
