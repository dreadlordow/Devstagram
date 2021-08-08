import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from devstagram.mainsite.models import Picture, Like, Comment, FriendRequest, Friendship
from tests.mainsite.login_and_create_picture import login_and_create_picture

UserModel = get_user_model()


class ProfileViewTests(TestCase):
    def setUp(self) -> None:
        self.user_one = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')
        self.user_two = UserModel.objects.create_user(username='test_two', email='test_two@abv.bg', password='12345qwe')
        self.client = Client()
        self.client.force_login(self.user_one)

    def test_user_profile_view_when_logged_in(self):
        profile_url = reverse('profile', kwargs={'slug': self.user_two.username})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['friendship'])
        self.assertFalse(response.context['is_friend_request_sent'])

        # Send a friend request to test if the context changes
        self.client.post(reverse('friend request'), data={
            'sender': self.user_one,
            'receiver': self.user_two
        })
        response_after_friend_request = self.client.get(profile_url)
        self.assertTrue(response_after_friend_request.context['is_friend_request_sent'])


class PictureUploadTests(TestCase):
    def test_upload_with_user_logged_in(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        picture = SimpleUploadedFile(name='test_image.jpg', content=open(settings.MEDIA_ROOT +
                                                                         '\\pictures\\test.jpg', 'rb').read(),
                                     content_type='image/jpeg')

        response = client.post(reverse('upload'), data={
            'picture': picture,
            'description': 'some description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_upload_without_user_logged_in(self):
        client = Client()
        picture = SimpleUploadedFile(name='test_image.jpg', content=open(settings.MEDIA_ROOT +
                                                                         '\\pictures\\test.jpg', 'rb').read(),
                                     content_type='image/jpeg')

        with self.assertRaises(Exception) as ex:
            client.post(reverse('upload'), data={
                'picture': picture,
                'description': 'some description'
            })


class PictureDisplayViewTests(TestCase):
    def setUp(self) -> None:
        self.user, self.client, pic = login_and_create_picture()
        self.client.force_login(self.user)
        self.picture = Picture.objects.first()

    def test_picture_display(self):
        picture_url = reverse('picture display', kwargs={'slug': self.user.username, 'pk': self.picture.id})
        response = self.client.get(picture_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['picture'], self.picture)


class PictureEditViewTests(TestCase):
    def setUp(self) -> None:
        self.user, self.client, pic = login_and_create_picture()
        self.picture = Picture.objects.first()

    def test_edit(self):
        self.assertEqual(Picture.objects.first().description, 'Test Description')

        edit_url = reverse('edit', kwargs={'pk': self.picture.id})
        response = self.client.get(edit_url)
        form = response.context['form']
        data = form.initial
        data['description'] = 'Edited description'

        edit_response = self.client.post(edit_url, data)

        self.assertEqual(edit_response.status_code, 302)
        self.assertEqual(edit_response.url, '/')
        self.assertEqual(Picture.objects.first().description, 'Edited description')


class PictureDeleteViewTests(TestCase):
    def setUp(self) -> None:
        self.user, self.client, pic = login_and_create_picture()
        self.picture = Picture.objects.first()

    def test_picture_delete(self):
        self.assertEqual(Picture.objects.all().count(), 1)

        response = self.client.post(reverse('delete picture', kwargs={'pk': self.picture.id}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/index/')
        self.assertEqual(Picture.objects.all().count(), 0)

        get_response = self.client.get(reverse('delete picture', kwargs={'pk': self.picture.id}))
        self.assertEqual(get_response.status_code, 400)


class LikePictureTests(TestCase):
    def setUp(self) -> None:
        self.user, self.client, pic = login_and_create_picture()
        self.picture = Picture.objects.first()

    def test_like(self):
        self.assertEqual(Like.objects.all().count(), 0)

        response = self.client.get(f'/like/{self.picture.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), 1)
        context = json.loads(response.content)['context']
        self.assertEqual(context['action'], 'like')
        self.assertEqual(context['likes'], 1)

    def test_unlike(self):
        # To test the unlike first we need to like the picture
        self.assertEqual(Like.objects.all().count(), 0)
        response = self.client.get(f'/like/{self.picture.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), 1)
        self.assertEqual(Like.objects.first().user, self.user)
        self.assertEqual(Like.objects.first().picture, self.picture)

        # Then we send the request again to unlike the picture
        unlike_response = self.client.get(f'/like/{self.picture.id}')

        context = json.loads(unlike_response.content)['context']

        self.assertEqual(context['action'], 'unlike')
        self.assertEqual(context['likes'], 0)

        self.assertEqual(unlike_response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), 0)


class CommentPictureViewTests(TestCase):
    def setUp(self) -> None:
        self.user, self.client,self.picture = login_and_create_picture()

    def test_comment_picture(self):
        picture = Picture.objects.first()
        self.assertEqual(Comment.objects.all().count(), 0)
        response = self.client.post(reverse('comment'), data={'pic_id':picture.id, 'comment': 'Test comment text'})
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Comment.objects.first().picture, picture)
        self.assertEqual(response.status_code, 302)

    def test_comment_picture_when_not_logged_in(self):
        client = Client()
        picture = Picture.objects.first()
        self.assertEqual(Comment.objects.all().count(), 0)
        response = client.post(reverse('comment'), data={'pic_id':picture.id, 'comment': 'Test comment text'})
        self.assertEqual(response.url, '/accounts/login/?next=/comment/')
        self.assertEqual(Comment.objects.all().count(), 0)


class DeleteCommentViewTests(TestCase):
    def setUp(self) -> None:
        self.user, self.client, self.picture = login_and_create_picture()

    def test_comment_delete(self):
        picture = Picture.objects.first()

        self.assertEqual(Comment.objects.all().count(), 0)

        # To delete a comment first we need to create it
        self.client.post(reverse('comment'), data={'pic_id': picture.id, 'comment': 'Test comment text'})
        self.assertEqual(Comment.objects.all().count(), 1)

        comment = Comment.objects.first()
        delete_response = self.client.post(reverse('delete comment', kwargs={'pk': comment.id}), data={'pic-pk': picture.id})

        self.assertEqual(delete_response.status_code, 302)
        self.assertEqual(Comment.objects.all().count(), 0)


class FriendRequestViewTests(TestCase):
    def setUp(self) -> None:
        self.user_one = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')
        self.user_two = UserModel.objects.create_user(username='test_two', email='test_two@abv.bg', password='12345qwe')
        self.client = Client()
        self.client.force_login(self.user_one)

    def test_friend_request_send(self):
        self.assertEqual(FriendRequest.objects.all().count(), 0)

        response = self.client.post(reverse('friend request'), data={
                    'sender': self.user_one,
                    'receiver': self.user_two
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/profile/{self.user_two.username}/')
        self.assertEqual(FriendRequest.objects.all().count(), 1)


class CreateFriendshipTests(TestCase):
    def setUp(self) -> None:
        self.user_one = UserModel.objects.create_user(username='test_one', email='test_one@abv.bg', password='12345qwe')
        self.user_two = UserModel.objects.create_user(username='test_two', email='test_two@abv.bg', password='12345qwe')
        self.client = Client()
        self.client.force_login(self.user_one)

    def test_create_friendship(self):
        self.assertEqual(Friendship.objects.all().count(), 0)

        self.client.post(reverse('friend request'), data={
            'sender': self.user_one,
            'receiver': self.user_two
        })
        # print(FriendRequest.objects.all())
        response = self.client.post(reverse('friendship'), data={
                        'sender': self.user_one.username,
                        'receiver': self.user_two.username,
                        'answer': 'accepted'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertEqual(Friendship.objects.all().count(), 1)

        friendship = Friendship.objects.first()
        self.assertEqual(str(friendship), f'{self.user_one.username} and {self.user_two.username}')
