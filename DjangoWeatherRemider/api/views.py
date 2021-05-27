from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from rest_framework.permissions import IsAdminUser

from .forms import RegistrationForm
from .models import City, Subscription
from .permissions import IsActive, IsOwner, IsReadOnly
from .serializers import CitySerializer, SubscriptionSerializer
from .utils import CLUDAPIView, TokenGenerator, post_method_required

# Create your views here.

# Class-based views


class SubscriptionView(CLUDAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsActive & IsOwner | IsAdminUser]


class CityView(CLUDAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsActive & IsReadOnly | IsAdminUser]

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            serialize(self.queryset.filter('json', name=request.GET)),
        )

# Function-based views


def auth_need(request):
    return HttpResponseForbidden(
        content=b'You must be authenticated for doing this',
        )


@post_method_required
def register(request):
    form = RegistrationForm(request.POST)
    if form.is_valid:
        account = form.save()
        account.is_active = False
        account.save()
        send_mail(
            subject='Confirm registration',
            message='',
            from_email='nutmegraw@yandex.ru',
            recipient_list=[account.email],
            html_message=render_to_string(
                'confirmation_message.html',
                context=dict(
                    host=request.get_host(),
                    account=account,
                    unique_string=TokenGenerator.make_token(account),
                    ),
                ),
            )
        return JsonResponse(dict(code=200))
    return HttpResponseForbidden(content=b'registration data is not valid')


@login_required
def confirm_registration(request, unique_string: str):
    if not TokenGenerator.check_token(request.user, unique_string):
        return HttpResponseForbidden(
            content=b'Something went wrong, the confirmation failed!',
            )
    request.user.is_active = True
    request.user.save()
    return JsonResponse(dict(code=200))
