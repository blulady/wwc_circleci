from django.urls import path, include
from rest_framework import routers

from .views import UserRegistrationView

urlpatterns = [
    path("registration/", UserRegistrationView.as_view()),
]