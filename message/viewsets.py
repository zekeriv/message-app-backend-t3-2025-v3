from rest_framework import viewsets

from message.models import Chat_room, Message
from message.serializers import Chat_roomSerializer, MessageSerializer


class Chat_roomViewSet(viewsets.ModelViewSet):
    queryset = Chat_room.objects.all()
    serializer_class = Chat_roomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer