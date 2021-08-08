from django.apps import apps

from devstagram.registration.apps import RegistrationConfig
from django.test import TestCase


class RegistrationConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(RegistrationConfig.name, 'devstagram.registration')