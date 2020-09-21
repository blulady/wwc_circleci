from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class mailSender(APIView):
    def post(self, request):
        
        subject = request.data.get('subject', '')
        message = request.data.get('message', '')
        fromEmail = request.data.get('fromEmail', '')
        toEmail = request.data.get('email', '')

        print('POST data=>'+ toEmail+':'+subject +":" + message+ ' :' + fromEmail)

        if subject and message  and toEmail:
            try:
                send_mail(subject, message, fromEmail, [toEmail])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return Response(status=status.HTTP_200_OK)
        else:
            return HttpResponse('Make sure all fields namely email,fromEmail,subject,message are entered and valid.')