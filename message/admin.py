from django.contrib import admin

from message.models import Chat_room, Message

# Register your models here.
admin.site.register(Chat_room)
admin.site.register(Message)

