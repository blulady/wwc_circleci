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
        result = self.validate_request(user_queryset, req['token'])
        if result['error']:
            return Response({'error': result['error']}, status=result['status'])
        try:
            user = result['user']
            serializer = UserSerializer(user,data=req['user'])
            if serializer.is_valid():
                password = make_password(req['user']['password'])
                serializer.save(password=password)
                user.userprofile.status = UserProfile.ACTIVE
                user.userprofile.save(update_fields=['status'])
                res_status = status.HTTP_201_CREATED
            else:
                error = serializer.errors
                res_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            error = "Something went wrong : {0}".format(e)
            res_status = res_status or status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response({'error': error}, status=res_status)

    def validate_request(self, user_queryset, request_token):
        result = {'error': None, 'user' : None, 'toke': None, 'status': None }
        if not user_queryset.exists():
            result['error'] = "User not created"
            result['status'] = status.HTTP_404_NOT_FOUND
            return result
        user = user_queryset.first()
        if not user.userprofile.is_new():
            result['error'] = 'User is already Active.'
            result['status'] = status.HTTP_400_BAD_REQUEST
            return result
        token_qs = RegistrationToken.objects.filter(token=request_token)
        if token_qs.exists():
            token = token_qs.first()
            if not token or token.user.email != user.email:
                result['error'] = 'Invalid token. Token Does not match the token generated for this user.'
                result['status'] = status.HTTP_400_BAD_REQUEST
                return result
        else:
            result['error'] = 'Token does not exist.'
            result['status'] = status.HTTP_400_BAD_REQUEST
            return result
        result['user'] = user
        result['token'] = token
        return result



