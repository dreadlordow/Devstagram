from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

UserModel = get_user_model()


class TestAuthentication(TestCase):

    def setUp(self):
        self.client = Client()
        self.email = 'georgi@abv.bg'
        self.password = '12345qwe'
        self.username = 'dreadlord'
        self.two_factor_authentication = False

    def test_user_signup_with_unused_email_and_username(self):
        response = self.client.post(reverse('register'), data={
            'username': 'testusername',
            'email': 'testemail@abv.bg',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
            'two_factor_authentication': False
        })
        users = get_user_model().objects.all().count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(users, 1)

    def test_user_signup_with_used_username(self):
        response = self.client.post(reverse('register'), data={
            'username': 'testusername',
            'email': 'testemail@abv.bg',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
            'two_factor_authentication': False
        })

        response2 = self.client.post(reverse('register'), data={
            'username': 'testusername',
            'email': 'testemail2@abv.bg',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
            'two_factor_authentication': False
        })
        self.assertEqual(response.status_code, 302)

        # Status code of the second request should be 200 because
        # the form did not submit successfully and it did not redirect
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(get_user_model().objects.all().count(), 1)

    def test_user_signup_with_used_email(self):
        response = self.client.post(reverse('register'), data={
            'username': 'testusername',
            'email': 'testemail@abv.bg',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
            'two_factor_authentication': False
        })

        response2 = self.client.post(reverse('register'), data={
            'username': 'testusername1',
            'email': 'testemail@abv.bg',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
            'two_factor_authentication': False
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(get_user_model().objects.all().count(), 1)


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(username='testusername')
        self.user.set_password('12345')
        self.user.save()

    def test_login(self):
        login = self.client.login(username='testusername', password='12345')
        self.assertTrue(login)

    def test_unsuccessfull_login(self):
        login = self.client.login(username='falseusername', password='12345')
        self.assertFalse(login)