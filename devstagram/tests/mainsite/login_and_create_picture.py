from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse


def login_and_create_picture():
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()
    client = Client()
    client.login(username='testuser', password='12345')
    picture = SimpleUploadedFile(name='test_image.jpg', content=open(settings.MEDIA_ROOT +
                                                                          '\\pictures\\test.jpg', 'rb').read(),
                                      content_type='image/jpeg')

    client.post(reverse('upload'), data={
        'picture': picture,
        'description': 'Test Description'
    })

    return user, client,picture
