from django.urls import path, include
from rest_framework import routers

from .views import UserRegistrationView

# router = routers.DefaultRouter()
# router.register("register", views.UserRegistrationView)

urlpatterns = [
    path("registration/", UserRegistrationView.as_view()),
    # path("registration/", include(router.urls)),
]