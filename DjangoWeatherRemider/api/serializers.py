from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        HiddenField, ModelSerializer)
from django.contrib.auth import get_user_model
from .models import City, Subscription


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email','password', )

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = get_user_model()(**validated_data)
        user.save()
        return user


class ConfirmSerializer(ModelSerializer):
    token = CharField(max_length=500)

    class Meta:
        model = get_user_model()
        fields = ['__all__']


class SubscriptionSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = '__all__'


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'
