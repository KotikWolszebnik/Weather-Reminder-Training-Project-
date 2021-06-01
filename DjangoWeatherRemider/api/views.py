from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from jwt import ExpiredSignatureError, decode, DecodeError
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import City, Subscription
from .permissions import IsActive, IsOwner, IsReadOnly
from .serializers import (CitySerializer, RegisterSerializer,
                          SubscriptionSerializer)
from .utils import CLUDAPIView

# Create your views here.

# Class-based views


class SubscriptionView(CLUDAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated & IsActive & IsOwner | IsAdminUser]


class CityView(CLUDAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated & IsActive & IsReadOnly | IsAdminUser]

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            serialize(
                'json',
                self.queryset.filter(name=request.GET['name']),
            ),
        )


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers,
        )

    def perform_create(self, serializer, request):
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        token = RefreshToken.for_user(user).access_token
        send_mail(
            subject='Confirm registration',
            message='',
            from_email='nutmegraw@yandex.ru',
            recipient_list=[user.email],
            html_message=render_to_string(
                'confirmation_message.html',
                context=dict(
                    host=request.get_host(),
                    account=user,
                    unique_string=str(token),
                    ),
                ),
            )


class ConfirmView(GenericAPIView):

    def get(self, request):
        try:
            payload = decode(
                request.GET.get('token'),
                settings.SECRET_KEY,
            )
            user = User.objects.get(id=payload['user_id'])
            user.is_active = True
            user.save()
            return Response(
                dict(email='Successfully activated'),
                status=status.HTTP_200_OK,
            )
        except ExpiredSignatureError:
            return Response(
                dict(error='Activation expired'),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DecodeError:
            return Response(
                dict(error='Invalid token'),
                status=status.HTTP_400_BAD_REQUEST,
            )
