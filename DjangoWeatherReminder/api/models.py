from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, BooleanField, CharField, EmailField,
                              ForeignKey, IntegerField, Model)
from .managers import UserManager

# Create your models here.


class Account(AbstractUser):
    username = None
    first_name = None
    last_name = None
    confirmed = BooleanField(default=False)
    email = EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Subscription(Model):
    NOTIFICATION_PERIODS = [
        (1, '1'), (3, '3'), (6, '6'), (12, '12'), (24, '24'),
    ]
    user = ForeignKey(
        get_user_model(), on_delete=CASCADE, related_name='subscriptions',
    )
    city = ForeignKey('City', on_delete=CASCADE)
    notification_period = IntegerField(choices=NOTIFICATION_PERIODS)

    class Meta:
        ordering = ['-id']


class City(Model):
    id = IntegerField(primary_key=True, unique=True)
    name = CharField(max_length=85)
    state_code = CharField(max_length=9, null=True)
    country = CharField(max_length=100, null=True)
    country_code = CharField(max_length=3, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'< City : {self.name} >'
