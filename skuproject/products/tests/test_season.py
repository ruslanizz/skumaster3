from django.test import Client
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from products.models import Season, Capsule, SKU, Size
from users.models import CustomUser


class SeasonTestCase(APITestCase):
    def setUp(self) -> None:
        self.testclient = Client()
        user=CustomUser.objects.create_user(email='test@test.ru', password='password')
        self.testclient.force_login(user=user)

        self.season_1=Season.objects.create(name='ЗИМА 2030',
                                            season_firstletters='230',
                                            id='1',
                                            user=user)

        self.capsule_1 = Capsule.objects.create(capsule_firstletters = '23002G',
                                                name = 'Сияющий свет',
                                                season = self.season_1,
                                                id = '2',
                                                user = user)

        self.sku_1 = SKU.objects.create(name = 'Толстовка',
                                        sku_firstletters = '23002GMC5606',
                                        capsule=self.capsule_1,
                                        id='3',
                                        user=user)


        self.size_1 = Size.objects.create(size_short='134',
                                          size_long='134*52*62',
                                          quantity_sold=25,
                                          quantity_instock=5,
                                          sellsumm_sold=3000,
                                          costsumm_sold=1200,
                                          income=1800,
                                          costsumm_instock=1800,
                                          sku_full='23002GMC5606-134*52*62',
                                          sku=self.sku_1,
                                          user=user)

        self.capsule_2 = Capsule.objects.create(capsule_firstletters = '23003G',
                                                name = 'Полночная звезда',
                                                season = self.season_1,
                                                id = '4',
                                                user = user)

        self.sku_2 = SKU.objects.create(name = 'Брюки',
                                        sku_firstletters = '23003GMC6303',
                                         capsule=self.capsule_2,
                                         id='5',
                                         user=user)


        self.size_2 = Size.objects.create(size_short='140',
                                          size_long='140*52*62',
                                          quantity_sold=10,
                                          quantity_instock=1,
                                          sellsumm_sold=2000,
                                          costsumm_sold=1000,
                                          income=1000,
                                          costsumm_instock=1100,
                                          sku_full='23003GMC6303-140*52*62',
                                          sku=self.sku_2,
                                          user=user)


    def test_login_page(self):
        response=self.testclient.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        response=self.testclient.get('/')
        self.assertEqual(response.status_code, 200)

    def test_capsule_page(self):
        response=self.testclient.get('/capsules/')
        self.assertEqual(response.status_code, 200)

    def test_capsules_quantity(self):
        url = reverse('seasons-list')
        response=self.testclient.get(url)
        calculated_data=response.data[0]['capsules_quantity']
        self.assertEqual(calculated_data,2)

    def test_capsules_sellsumm_sold(self):
        url = reverse('seasons-list')
        response=self.testclient.get(url)
        calculated_data=response.data[0]['capsules_sellsumm_sold']
        self.assertEqual(calculated_data,5000)

    def test_capsules_costsumm_sold(self):
        url = reverse('seasons-list')
        response=self.testclient.get(url)
        calculated_data = response.data[0]['capsules_costsumm_sold']
        self.assertEqual(calculated_data, 2200)

    def test_capsules_income(self):
        url = reverse('seasons-list')
        response=self.testclient.get(url)
        calculated_data = response.data[0]['capsules_income']
        self.assertEqual(calculated_data, 2800)

    def test_capsules_costsumm_instock(self):
        url = reverse('seasons-list')
        response=self.testclient.get(url)
        calculated_data = response.data[0]['capsules_costsumm_instock']
        self.assertEqual(calculated_data, 2900)

    def test_capsules_margin_percent(self):
        url = reverse('seasons-list')
        response=self.testclient.get(url)
        calculated_data = response.data[0]['capsules_margin_percent']
        self.assertEqual(calculated_data, 127)












