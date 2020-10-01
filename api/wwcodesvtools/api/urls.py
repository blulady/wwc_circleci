from django.urls import path, include
from .views import UserRegistrationView, MailSender

urlpatterns = [
    path("registration/", UserRegistrationView.as_view()),
    path("send_email_example/", MailSender.as_view()),
]
