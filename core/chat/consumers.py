import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async



from .models import Message, Chat, Group, User

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Add room group to channel layer
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Add notification group to channel layer
        
        await self.channel_layer.group_add(
            'notifications',
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
        datetime = text_data_json['datetime']
        
        await self.save_message(username, chatname, message)

        # Send data to Room Group on channel layer
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chatroom_message',
                'message': message,
                'username': username,
                'chatname': chatname,
                'datetime': datetime
            }
        )

        # Send Notofications to Room Group on channel layer
        await self.channel_layer.group_send(
            'notifications',
            {
                'type' : 'lala',
                'message': message,
                'username': username,
                'chatname': chatname,
                'datetime': datetime
            }
        )
    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        chatname = event['chatname']
        datetime = event['datetime']
        
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'chatname':chatname,
            'datetime':datetime,
        }))

    async def lala(self, event):
        message = 'noti'
        username = 'noti'
        chatname = 'noti'
        datetime = 'noti'
        
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'chatname':chatname,
            'datetime':datetime,
        }))

    @sync_to_async
    def save_message(self, username, chatname, message):
        
        if type(chatname) == int:
            group = Group.objects.get(id=chatname)
            user = User.objects.get(username=username)

            group_message = Message.objects.create(
                                                    user=user,
                                                    group=group,
                                                    body=message,
                                                )

            group.last_message = f'{message[:20]}...' if len(message) > 20 else f'{message}'
            group.last_message_time = group_message.updated
            group.save()
        
        else:
            user = User.objects.get(username=username)
            chats = Chat.objects.filter(name=chatname)

            chat_message = Message.objects.create(user=user, body=message)
            chat_message.chats.set(chats)
            chats[0].last_message = f'{message[:20]}...' if len(message) > 20 else f'{message}'
            chats[1].last_message = f'{message[:20]}...' if len(message) > 20 else f'{message}'
            chats[0].last_message_time = chat_message.updated
            chats[1].last_message_time = chat_message.updated
            chat_message.save()
            chats[0].save()
            chats[1].save()

class A(AsyncWebsocketConsumer):
    async def conect(self):
        await self.accept()