import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer, AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User

from devstagram.async_chat.models import ChatRoom, Message
from devstagram.mainsite.models import ProfilePicture


class ChatRoomConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def get_picture(self, user):
        return ProfilePicture.objects.get(user=user)

    @database_sync_to_async
    def get_chatroom(self, user_one, user_two):
        chatroom = ChatRoom.objects.filter(user_one=user_one, user_two=user_two)|ChatRoom.objects.filter(user_one=user_two, user_two=user_one)
        return chatroom[0]

    @database_sync_to_async
    def create_message(self, chatroom, sender, receiver, message):
        message_created = Message(chatroom=chatroom, sender=sender, receiver=receiver ,message=message)
        message_created.save()
        chatroom.update_last_msg_time()
        return message_created

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_one'] + '-' + self.scope['url_route']['kwargs']['user_two']
        self.room_group_name = 'asyncchat_%s' % self.room_name

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

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['sender']
        receiver = text_data_json['receiver']

        user = await self.get_user(username)
        receiver = await self.get_user(receiver)

        chatroom = await self.get_chatroom(user, receiver)
        created_message = await self.create_message(chatroom, user, receiver, message)
        timestamp_obj = created_message.timestamp
        timestamp = f'{timestamp_obj.hour}:{timestamp_obj.minute}'

        picture = await self.get_picture(user)
        receiver_picture = await self.get_picture(receiver)

        picture_url = picture.image.url
        receiver_picture_url = receiver_picture.image.url

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
                'pictureurl': picture_url,
                'receiver_picture_url': receiver_picture_url,
                'timestamp': timestamp
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        pictureurl = event['pictureurl']
        receiver_picture_url = event['receiver_picture_url']
        timestamp = event['timestamp']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'pictureurl': pictureurl,
            'receiver_picture_url': receiver_picture_url,
            'timestamp': timestamp
        }))


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('connected')
        await self.accept()
        await self.channel_layer.group_add('gossip', self.channel_name)
        # await self.send({
        #     "type": "websocket.accept"
        # })

    async def disconnect(self, code):
        await self.channel_layer.group_discard('gossip', self.channel_name)

    async def message_gossip(self, event):
        await self.send(text_data=json.dumps(event))
