from django.contrib.auth import get_user_model
from rest_framework.serializers import (CurrentUserDefault, HiddenField,
                                        ModelSerializer)

from .models import City, Subscription


class AccountSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', )

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class SubscriptionSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = '__all__'


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'
