# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import CustomUser, Message, Group
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'group_{self.group_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        type=data.get('type')
        if(type=='like_message'):
            userid=self.scope['user'].id
            messageid=data['message_id']
            count=await self.update_like_count(userid,messageid)
            await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'like_message',
                'count': count,
                'messageid': data['message_id'],
            }
        )
        if type=='chat':
           message=data['message']
           username = self.scope['user'].username
           groupid = self.scope['url_route']['kwargs']['group_id']
           message_object=await self.save_message(username, groupid, message)

           await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'messageid':message_object.id,
                'count':message_object.likes
            }
        )
   
    async def like_message(self,event):
        count=event['count']
        messageid=event['messageid']
        await self.send(text_data=json.dumps({

            'type':'like_message',
            'count':count,
            'messageid':messageid
        }))


    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        messageid=event['messageid']
        count=event['count']

        await self.send(text_data=json.dumps({
            'message': message,
            'username':username,
            'messageid':messageid,
            'count':count
            
        }))

    

    @sync_to_async
    def save_message(Self, username, group, message):
        user = CustomUser.objects.get(username=username)
        group = Group.objects.get(id=group)
        message =Message.objects.create(user=user, group=group, content=message)
        return message

    @sync_to_async
    def update_like_count(self,userid, messageid):
        message_object=Message.objects.get(id=messageid)
        message_object.likes+=1
        message_object.save()
        return message_object.likes
   