from django.urls import path
from api.views.UserRegistrationView import UserRegistrationView
from api.views.MailSender import MailSender
from api.views.AddMemberView import AddMemberView
from api.views.GetMembersView import GetMembersView, GetMemberInfoView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("registration/", UserRegistrationView.as_view()),
    path("send_email_example/", MailSender.as_view()),
    path("login", TokenObtainPairView.as_view()),
    path("login/refresh", TokenRefreshView.as_view()),
    path("add_member/", AddMemberView.as_view()),
    path("get_members/", GetMembersView.as_view()),
    path('get_member_info/<int:id>', GetMemberInfoView.as_view()),
]
