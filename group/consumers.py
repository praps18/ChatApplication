# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

from .models import CustomUser, Like, Message, Group
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
            user=self.scope['user']
            messageid=data['message_id']
            count=await self.update_like_count(user,messageid)
            liked_users=await self.get_liked_usernames(messageid)
            await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'like_message',
                'count': count,
                'messageid': data['message_id'],
                'liked_user':liked_users
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
        liked_users=event['liked_user']
        await self.send(text_data=json.dumps({

            'type':'like_message',
            'count':count,
            'messageid':messageid,
            'liked_users':liked_users
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
    def update_like_count(self,user, messageid):
        message = get_object_or_404(Message, id=messageid)
        like, created = Like.objects.get_or_create(user=user, message=message)
        if created:
            message.likes+=1
            message.save()
            return message.likes
        else:
            message.likes-=1
            message.save()
            like.delete()
            return message.likes 
        
    @sync_to_async
    def get_liked_usernames(self,message_id):
        try:
            message = Message.objects.get(id=message_id)
            liked_users = Like.objects.filter(message=message).values_list('user__username', flat=True)
            return list(liked_users)
        except Message.DoesNotExist:
            return []
          
       
   