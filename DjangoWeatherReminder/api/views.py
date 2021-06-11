from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import City, Subscription
from .permissions import IsConfirmed, IsOwner, IsReadOnly
from .serializers import (AccountSerializer, CitySerializer,
                          SubscriptionSerializer)
from .utils import TokenGenerator

# Create your views here.

# Class-based views


class SubscriptionView(ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated & IsConfirmed & IsOwner | IsAdminUser]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class CityView(ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated & IsConfirmed & IsReadOnly | IsAdminUser]

    def get_queryset(self):
        city_name = self.request.GET['name']
        if city_name is not None:
            queryset = City.objects.filter(name=city_name)
        return queryset


class RegisterView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

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
        user = get_user_model().objects.get(email=serializer.data['email'])
        token = TokenGenerator.make_token(user)
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
                    unique_string=token,
                    ),
                ),
            )


class ConfirmView(APIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = kwargs['token']
        if not TokenGenerator.check_token(request.user, token):
            return Response(
                dict(error='Something went wrong, the confirmation failed!'),
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            request.user.confirmed = True
            request.user.save()
            return Response(
                dict(message="You've got confirming success."),
                status=status.HTTP_200_OK,
            )
