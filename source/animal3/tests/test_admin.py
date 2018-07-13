
import re

from django.contrib.auth.models import User
from django.test import TestCase


class TestCaseAdmin(TestCase):
    """Create admin user, login as same"""
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_user(self.username, '', self.password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        self.client.logout()


class AdminNotLoggedInTest(TestCase):
    def test_home(self):
        """Login form printed and customised"""
        response = self.client.get('/admin/')
        self.assertTemplateUsed(response, 'admin/login.html')
        self.assertEqual(re.search('django', response.content, re.I), None,
            "Page contains 'django'.  Replace with your site's title.")


class AdminLoggedInTest(TestCaseAdmin):
    def test_is_admin(self):
        """Tests running as admin user"""
        self.assertTrue(isinstance(self.user, User))
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

    def test_home(self):
        response = self.client.get('/admin/')
        self.assertTemplateUsed(response, 'admin/index.html')
        self.assertEqual(re.search('django', response.content, re.I), None,
            "Page contains 'django'.  Replace with your site's title.")
