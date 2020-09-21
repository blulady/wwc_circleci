from django.urls import path, include
from rest_framework import routers
from .views import mailSender

urlpatterns = [
    path("sendEmail_example/", mailSender.as_view()),
] 
