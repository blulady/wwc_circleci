from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserRegistrationView, MailSender


urlpatterns = [
    path("registration/", UserRegistrationView.as_view()),
    path("send_email_example/", MailSender.as_view()),
    path("login", TokenObtainPairView.as_view()),
    path("login/refresh", TokenRefreshView.as_view()),
]
