"""DjangoWeatherRemider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CityView, RegisterView, ConfirmView, SubscriptionView

urlpatterns = [
    # path to simplejwt end points
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view()),
    path('confirm/<str:token>/', ConfirmView.as_view()),

    path('city/search_by_name/', CityView.as_view()),

    path('subscription/', SubscriptionView.as_view()),
    path('subscription/all/', SubscriptionView.as_view()),
    path('subscription/<int:pk>/', SubscriptionView.as_view()),
]
