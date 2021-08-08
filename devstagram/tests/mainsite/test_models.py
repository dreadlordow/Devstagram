from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from devstagram import settings
from devstagram.mainsite.models import FriendRequest, Friendship, UserFriends, Like, Picture, TwoFactorAuthMsg, \
    UserAuth, ProfilePicture, Comment

UserModel = get_user_model()


class UserAuthTests(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')

    def test_user_auth(self):
        user_auth = UserAuth(user=self.user, two_factor_auth=False)
        user_auth.full_clean()
        user_auth.save()


class TwoFactorAuthMsgTests(TestCase):

    def test_two_factor_msg(self):
        two_factor = TwoFactorAuthMsg(hash_url='1234567qwe', two_factor_code=83291)
        two_factor.full_clean()
        two_factor.save()


class PictureTests(TestCase):
    def setUp(self) -> None:
        self.picture = SimpleUploadedFile(name='test_image.jpg', content=open(settings.MEDIA_ROOT +
                                                                              '\\pictures\\test.jpg', 'rb').read(),
                                          content_type='image/jpeg')
        self.user = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')

    def test_picture(self):
        picture = Picture(user=self.user, description='Some description')
        picture.picture = self.picture
        picture.full_clean()
        picture.save()


class FriendRequestTests(TestCase):
    def setUp(self) -> None:
        self.user_one = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')
        self.user_two = UserModel.objects.create_user(username='test_two', email='test_two@abv.bg', password='12345qwe')

    def test_friend_request_send(self):
        friend_request = FriendRequest(sender=self.user_two, receiver=self.user_two)
        friend_request.full_clean()
        friend_request.save()


class FriendshipTests(TestCase):
    def setUp(self) -> None:
        self.user_one = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')
        self.user_two = UserModel.objects.create_user(username='test_two', email='test_two@abv.bg', password='12345qwe')

    def test_friendship(self):
        friendship = Friendship(friend_one=self.user_one, friend_two=self.user_two)
        friendship.full_clean()
        friendship.save()


class UserFriendsTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')

    def test_user_friends(self):
        friends = UserFriends(user=self.user, friends=10)
        friends.full_clean()
        friends.save()

        self.assertEqual(friends.friends, 10)


class LikeTests(TestCase):
    def setUp(self) -> None:
        self.picture = SimpleUploadedFile(name='test_image.jpg', content=open(settings.MEDIA_ROOT +
                                                                              '\\pictures\\test.jpg', 'rb').read(),
                                          content_type='image/jpeg')
        self.user = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')

    def test_like(self):
        picture = Picture(user=self.user, description='Some description')
        picture.picture = self.picture
        picture.save()
        like = Like(picture=picture, user=self.user)
        like.full_clean()
        like.save()
        self.assertEqual(str(like), f"{self.user.username} liked {self.user.username}'s picture")


class ProfilePictureTests(TestCase):
    def setUp(self) -> None:
        self.picture = SimpleUploadedFile(name='test_image.jpg', content=open(settings.MEDIA_ROOT +
                                                                              '\\pictures\\test.jpg', 'rb').read(),
                                          content_type='image/jpeg')
        self.user = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')

    def test_profile_picture(self):
        profile_picture = ProfilePicture(user=self.user)
        profile_picture.image = self.picture
        profile_picture.full_clean()
        profile_picture.save()


class CommentTests(TestCase):
    def setUp(self) -> None:
        self.picture = SimpleUploadedFile(name='test_image.jpg', content=open(settings.MEDIA_ROOT +
                                                                              '\\pictures\\test.jpg', 'rb').read(),
                                          content_type='image/jpeg')
        self.user = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')

    def test_comment(self):
        picture = Picture(user=self.user, description='Some description')
        picture.picture = self.picture
        picture.save()
        comment = Comment(picture=picture, user=self.user, comment='Some comment')
        comment.full_clean()
        comment.save()