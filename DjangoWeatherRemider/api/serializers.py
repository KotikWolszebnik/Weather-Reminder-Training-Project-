from django.contrib.auth.models import User
from rest_framework.serializers import (CurrentUserDefault, HiddenField,
                                        ModelSerializer)

from .models import City, Subscription


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['email'],
            is_active=False,
            **validated_data,
        )


class SubscriptionSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = '__all__'


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'
