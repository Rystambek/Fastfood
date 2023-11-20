from django.test import TestCase
from django.urls import reverse
from .models import CustomUser
# Create your tests here.

class SignupTestCase():
    def test_signup_view(self):
        response = self.client.post(
            reverse('users:signup'),
            data = {
                'firstname':'Aslbek',
                'username':'Aslbek',
                'email':' ',
                'password1':'qweqweqwe',
                'password2':'qweqweqwe',
            }
        )
        user=CustomUser.objects.get(username='Aslbek')
        self.assertEqual(user.first_name, 'Aslbek')
        self.assertEqual(user.email, ' ')
        self.assertTrue(user.check_password('qweqweqew'))