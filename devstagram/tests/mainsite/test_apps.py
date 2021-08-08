from django.apps import apps

from devstagram.mainsite.apps import MainsiteConfig
from django.test import TestCase

class MainsiteConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(MainsiteConfig.name, 'devstagram.mainsite')
