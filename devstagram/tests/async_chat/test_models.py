from django.contrib.auth import get_user_model

from django.test import TestCase, Client

from devstagram.async_chat.models import ChatRoom, Message, PostMessage
from devstagram.mainsite.models import Picture
from tests.mainsite.login_and_create_picture import login_and_create_picture

UserModel = get_user_model()

class ChatRoomTest(TestCase):
    def setUp(self) -> None:
        self.user_one = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')
        self.user_two = UserModel.objects.create_user(username='test_two', email='test_two@abv.bg', password='12345qwe')

    def test_chatroom(self):
        chatroom = ChatRoom(user_one=self.user_one,user_two=self.user_two)
        chatroom.full_clean()
        chatroom.save()


class MessageTest(TestCase):
    def setUp(self) -> None:
        self.user_one = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')
        self.user_two = UserModel.objects.create_user(username='test_two', email='test_two@abv.bg', password='12345qwe')

    def test_message(self):
        chatroom = ChatRoom(user_one=self.user_one,user_two=self.user_two)
        chatroom.save()
        sender = self.user_one
        receiver = self.user_two
        message = 'Some message'

        message = Message(chatroom=chatroom, sender=sender, receiver=receiver, message=message)
        message.full_clean()
        message.save()


class PostMessageTest(TestCase):
    def setUp(self) -> None:
        self.user_one, self.client, picture = login_and_create_picture()
        self.user_two = UserModel.objects.create_user(username='test_two', email='test_two@abv.bg', password='12345qwe')
        self.chatroom = ChatRoom(user_one=self.user_one,user_two=self.user_two)
        self.chatroom.save()
        self.picture = Picture.objects.first()

    def test_postmessage(self):
        postmessage = PostMessage(chatroom=self.chatroom, sender=self.user_one, post_owner=self.user_one, post_image=self.picture)
        postmessage.full_clean()
        postmessage.save()