import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async



from .models import Message, Chat, Group, User, Notifications

users_online = []

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
                
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        await self.add_users_to_online(self.user, self.room_name)



    async def disconnect(self, close_code):
        await self.remove_users_from_online(self.user, self.room_name)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def add_users_to_online(self, user, room):
        users_online.append([user.id, room])


    @sync_to_async
    def remove_users_from_online(self, user, room):
        users_online.remove([user.id, room])

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chatname = text_data_json['chatname']
        datetime = text_data_json['datetime']
        
        await self.save_message(username, chatname, message)

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

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['userId']
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
        chatname = text_data_json['chatname']
        from_to = text_data_json['from_to']
        to = text_data_json['to']

        send = True
        for info in users_online:
            if int(to) == info[0] and chatname == info[1]:
                send = False
                print('no send')
       
        print(send)
        if send:
            print('se envio')
            await self.sum_unread_notification(to, from_to, chatname)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'notification',
                'chatname' : chatname,
                'from_to': from_to,
                'to': to,
            }
        )

    async def notification(self, event):
        chatname = event['chatname']
        from_to = event['from_to']
        to = event['to']
        
        send = True
        for info in users_online:
            if int(to) == info[0] and chatname == info[1]:
                send = False
       
        if send:
            await self.send(text_data=json.dumps({
                'chatname': chatname,
                'from_to': from_to,
                'to': to,
            }))

    @sync_to_async
    def sum_unread_notification(self, userId, user2Id, chatname):
        
        to_user = User.objects.get(id=userId)
        from_user = User.objects.get(id=user2Id)


        to_user.unread_notifications += 1
        to_user.save()

        chat_name = chatname
        # order_list=sorted([from_user.id, to_user.id])
        # chat_name = f'{order_list[0]}_chat_{order_list[1]}'

        chat_to_notificate = Chat.objects.get(name=chat_name, user_1=to_user)

        
        link = f'chat/conversation/{chat_name}'
        
        try:
            notification = Notifications.objects.get(
               
                from_to=from_user,
                to=to_user,
                
                )
            
            notification.count += 1
            notification.save()

        except:

            notification = Notifications.objects.create(
                chat=chat_to_notificate, 
                from_to=from_user,
                to=to_user,
                link=link,
                )

