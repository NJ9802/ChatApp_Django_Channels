import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User

from .models import Message, Chat, Group

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
       

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chatname = text_data_json['chatname']

        await self.save_message(username, chatname, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chatroom_message',
                'message': message,
                'username': username,
                'chatname': chatname,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        chatname = event['chatname']
        
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'chatname':chatname,
        }))

    @sync_to_async
    def save_message(self, username, chatname, message):

        user = User.objects.get(username=username)
        chats = Chat.objects.filter(name=chatname)

        message = Message.objects.create(user=user, body=message)
        message.chats.set(chats)
        message.save()
