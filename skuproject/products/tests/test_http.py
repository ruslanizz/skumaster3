from django.test import Client
from rest_framework.test import APITestCase
from users.models import CustomUser


class HttpTestCase(APITestCase):
    def setUp(self) -> None:
        self.testclient = Client()
        user=CustomUser.objects.create_user(email='test@test.ru', password='password')
        self.testclient.force_login(user=user)

    def test_login_page(self):
        response=self.testclient.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        response=self.testclient.get('/')
        self.assertEqual(response.status_code, 200)

    def test_capsule_page(self):
        response=self.testclient.get('/capsules/')
        self.assertEqual(response.status_code, 200)

    def test_sku_page(self):
        response=self.testclient.get('/sku/')
        self.assertEqual(response.status_code, 200)














