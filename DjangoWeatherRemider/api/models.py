from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, CharField, DateTimeField, EmailField,
                              ForeignKey, IntegerField, Model)

# Create your models here.


class Account(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    username = None
    email = EmailField(unique=True)
    reg_confirmed_date = DateTimeField(auto_now=False, null=True)

    def __str__(self):
        return f'< Account : {self.email} >'


class Subscription(Model):
    NOTIFICATION_PERIODS = [
        (1, '1'),
        (3, '3'),
        (6, '6'),
        (12, '12'),
        (24, '24'),
    ]
    account = ForeignKey(Account, on_delete=CASCADE, related_name='subscriptions')
    city = ForeignKey('City', on_delete=CASCADE)
    notification_period = IntegerField(choices=NOTIFICATION_PERIODS)


class City(Model):
    id = IntegerField(primary_key=True, unique=True)
    name = CharField(max_length=85)
    state_code = CharField(max_length=9, null=True)
    country = CharField(max_length=20, null=True)
    country_code = CharField(max_length=3, null=True)

    def __str__(self):
        return f'< City : {self.name} >'
