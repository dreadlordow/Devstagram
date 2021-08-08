from django.apps import apps

from devstagram.async_chat.apps import AsyncChatConfig
from django.test import TestCase


class AsyncChatConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(AsyncChatConfig.name, 'devstagram.async_chat')