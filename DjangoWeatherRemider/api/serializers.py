from rest_framework.serializers import (CurrentUserDefault, HiddenField,
                                        ModelSerializer)

from .models import Subscription, City


class SubscriptionSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = '__all__'


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'
