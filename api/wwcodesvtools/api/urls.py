from django.urls import path
from api.views.UserRegistrationView import UserRegistrationView
from api.views.MailSender import MailSender
from api.views.AddMemberView import AddMemberView
from api.views.GetMembersView import GetMembersView, GetMemberInfoView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from .swagger import login_response as resp
from api.views.CustomTokenObtainPairView import CustomTokenObtainPairView
from api.views.LogoutView import LogoutView
from api.views.DeleteMemberView import DeleteMemberView

decorated_login_view = \
    swagger_auto_schema(
        method='post',
        responses=resp.response
    )(CustomTokenObtainPairView.as_view())

urlpatterns = [
    path("user/activate/", UserRegistrationView.as_view()),
    path("send_email_example/", MailSender.as_view()),
    path("login", decorated_login_view),
    path("login/refresh", TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path("user/create/", AddMemberView.as_view()),
    path("users/", GetMembersView.as_view()),
    path('user/<int:id>', GetMemberInfoView.as_view()),
    path('user/delete/<int:id>', DeleteMemberView.as_view()),
]
