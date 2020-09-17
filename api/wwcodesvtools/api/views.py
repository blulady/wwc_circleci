from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, RegistrationToken
from .serializers import UserSerializer

# Create your views here.

class UserRegistrationView(APIView):

    def post(self, request, format=None):
        res_status = None
        error = None
        req = request.data
        user_queryset = User.objects.select_related('userprofile').filter(email=req['user']['email'])
        if not user_queryset.exists():
            error = "User not created"
            res_status = status.HTTP_404_NOT_FOUND
            return Response({'error': error}, status=res_status)
        try:
            user = user_queryset.first()
            error = self.validate_request(user, req['token'])
            serializer = UserSerializer(user,data=req['user'])
            if not error and serializer.is_valid():
                password = make_password(req['user']['password'])
                serializer.save(password=password)
                user.userprofile.status = UserProfile.ACTIVE
                user.userprofile.save(update_fields=['status'])
                res_status = status.HTTP_201_CREATED
            else:
                error = error or "Invalid Data"
                res_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            error = "Something went wrong : {0}".format(e)
            res_status = res_status or status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response({'error': error}, status=res_status)

    def validate_request(self, user, request_token):
        if not user.userprofile.is_new():
            return 'User is already Active.'
        token_qs = RegistrationToken.objects.filter(token=request_token)
        if token_qs.exists():
            token = token_qs.first()
            if not token or token.user.email != user.email:
                return 'Invalid token. Token Does not match the token generated for this user.'
        else:
            return 'Token does not exist.'
        return None



