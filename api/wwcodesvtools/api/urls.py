from django.urls import path
from .views import UserRegistrationView, MailSender, AddMemberView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("registration/", UserRegistrationView.as_view()),
    path("send_email_example/", MailSender.as_view()),
    path("login", TokenObtainPairView.as_view()),
    path("login/refresh", TokenRefreshView.as_view()),
    path("add_member/", AddMemberView.as_view()),
]
