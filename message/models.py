from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Chat_room(models.Model):
    name = models.CharField(max_length=100)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ManyToManyField(User, related_name="message_receivers", null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_room = models.ForeignKey(Chat_room, on_delete=models.CASCADE)
