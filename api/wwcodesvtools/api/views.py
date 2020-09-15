# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, RegistrationToken
from .serializers import UserSerializer

# Create your views here.

class UserRegistrationView(APIView):

    def post(self, request, format=None):
        req = request.data
        user_queryset = User.objects.select_related('userprofile').filter(email=req['user']['email'])
        res_status = None
        error = None
        try:
            if user_queryset.exists():
                user = user_queryset.first()
                if not user.userprofile.is_new():
                    res_status = status.HTTP_400_BAD_REQUEST
                    raise Exception('User already registered')
                token = RegistrationToken.objects.get(token=req['token'])
                if not token or token.user.email != user.email:
                    res_status = status.HTTP_400_BAD_REQUEST
                    raise Exception('Invalid token. Token Does not match the token generated for this user.')
                serializer = UserSerializer(user,data=req['user'])
                if serializer.is_valid():
                    serializer.save()
                    user.userprofile.status = UserProfile.ACTIVE
                    user.userprofile.save(update_fields=['status'])
                    res_status = status.HTTP_201_CREATED
                else: 
                    error = "Invalid Data"
                    res_status = status.HTTP_400_BAD_REQUEST
            else:
                error = "User not created"
                res_status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            error = "Something went wrong : {0}".format(e)
            res_status = res_status or status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response({'error': error}, status=res_status)
    


