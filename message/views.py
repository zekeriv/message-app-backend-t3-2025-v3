from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from message.models import Message
from message.serializers import MessageSerializer


# Create your views here.
@api_view(['POST'])
def send_message(request):
    message_serializer = MessageSerializer(data=request.data)
    if message_serializer.is_valid():
        message_serializer.save()
        return Response({'message': 'Message sent successfully'},
                        status=status.HTTP_201_CREATED)
    else:
        return Response(message_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=200)

