from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class InspectLoginPage(TestCase):
    def test_status_code(self):
        '''Checking if Status Code on Login Page == 200 '''

        login = self.client.get(reverse('login'))

        self.assertEqual(login.status_code, 200)