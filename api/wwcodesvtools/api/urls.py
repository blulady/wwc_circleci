from django.urls import path, include
from .views import UserRegistrationView, mailSender

urlpatterns = [
    path("registration/", UserRegistrationView.as_view()),
    path("sendEmail_example/", mailSender.as_view()),
]
