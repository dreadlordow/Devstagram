from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views import generic as views
from django.shortcuts import render
from django.db import connection

from devstagram.chat.models import ChatRoom, Message
from devstagram.mainsite.models import ProfilePicture


class CreateOrGetChatRoom(views.View):

    def action(self, request, *args, **kwargs):
        user_one = request.user
        user_two_username = kwargs.get('slug')
        user_two = User.objects.get(username=user_two_username)
        try:
            chatroom = ChatRoom.objects.filter(user_one=user_one, user_two=user_two)|ChatRoom.objects.filter(user_one=user_two, user_two=user_one)
            chatroom = chatroom[0]
        except IndexError:
            chatroom = ChatRoom(user_one=user_one, user_two=user_two)
            chatroom.save()


        messages = Message.objects.filter(sender=user_one, receiver=user_two) \
                   | Message.objects.filter(sender=user_two, receiver=user_one)
        msgs = chatroom.message_set.all()

        context = {
            'messages': msgs,
            'receiver': user_two,
            'chatroom': chatroom,
            'chatroom_id': chatroom.id,
            'receiver_pfp': ProfilePicture.objects.get(user=user_two),
            'sender_pfp': ProfilePicture.objects.get(user=user_one)
        }
        return context

    def post(self, request, *args, **kwargs):
        context = self.action(request, *args ,**kwargs)
        return render(request, 'chat/chat.html', context)

    def get(self, request, *args, **kwargs):
        context = self.action(request, *args ,**kwargs)
        return render(request, 'chat/chat.html', context)


class SendMessage(views.View):

    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver = User.objects.get(username=request.POST['receiver'])
        message = request.POST['message']
        chatroom_id = request.POST['chatroom_id']
        chatroom = ChatRoom.objects.get(pk=chatroom_id)
        chatroom.update_last_msg_time()
        chatroom.save()

        message = Message(message=message,sender=sender, receiver=receiver, chat_room=chatroom)
        message.save()
        messages = list(chatroom.message_set.all())
        context = {
            'messages': messages,
            'receiver': receiver,
            'chatroom': chatroom,
            'chatroom_id': chatroom_id,
            'receiver_pfp': ProfilePicture.objects.get(user=receiver),
            'sender_pfp': ProfilePicture.objects.get(user=sender)
        }
        return render(request, 'chat/chat.html', context)

