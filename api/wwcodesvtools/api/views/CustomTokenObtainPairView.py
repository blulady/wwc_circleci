from api.serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns the authenticated user data,
    and the access, refresh JSON web token pair to prove the authentication of those credentials

    """
    # Replace the serializer with the custom
    serializer_class = CustomTokenObtainPairSerializer
