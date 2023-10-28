from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CustomSessionLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusername', password='testpassword')

    def test_custom_session_login(self):
        self.client.login(username='testusername', password='testpassword')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)