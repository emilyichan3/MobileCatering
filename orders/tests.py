from django.test import TestCase, Client
from django.contrib.auth import get_user_model  
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from .models import Order, Menu, Caterer

TEST_EMAIL = 'testuser2@gmail.com'
TEST_PASSWORD = 'occie2025'
TEST_PERMISSION = 'add_caterer' 

class UserPermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(email=TEST_EMAIL, password=TEST_PASSWORD)
        permission = Permission.objects.get(codename=TEST_PERMISSION)  # Ensure this permission exists
        cls.user.user_permissions.add(permission)

    def test_user_permissions(self):
        self.assertTrue(self.user.has_perm(f'orders.{TEST_PERMISSION}'))

class CatererModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(email=TEST_EMAIL, password=TEST_PASSWORD)
        cls.caterer = Caterer.objects.create(
            register=cls.user,
            caterer_name='Test Caterer',
            caterer_description='This is a test caterer',
            location='Test Centre'
        )

    def test_caterer_content(self):
        caterer = Caterer.objects.get(pk=1)
        self.assertEqual(caterer.register.email, TEST_EMAIL)
        self.assertEqual(caterer.caterer_name, 'Test Caterer')
        self.assertEqual(caterer.caterer_description, 'This is a test caterer')
        self.assertEqual(caterer.location, 'Test Centre')

    def test_caterer_str_method(self):
        caterer = Caterer.objects.get(pk=1)
        self.assertEqual(str(caterer), f'{ caterer.caterer_name } is located at { caterer.location }')
        

    def test_get_absolute_url(self):
        caterer = Caterer.objects.get(pk=1)
        self.assertEqual(caterer.get_absolute_url(), reverse('orders-mycaterer', args=[caterer.register.id]))


class OrdersViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email=TEST_EMAIL, password=TEST_PASSWORD)
        permission = Permission.objects.get(codename=TEST_PERMISSION)  # Ensure this permission exists
        self.user.user_permissions.add(permission)

        self.caterer = Caterer.objects.create(
            register=self.user,
            caterer_name='Test Caterer',
            caterer_description='This is a test caterer',
            location='Test Centre'
        )

    def test_CatererListView(self):
        url = reverse('orders-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test caterer')
        self.assertTemplateUsed(response, 'orders/home.html')

    def test_MyCatererCreateView(self):
        self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        get_response = self.client.get(reverse('orders-mycaterer-new'))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'orders/myCaterer_form.html')

        caterer_response = self.client.post(reverse('orders-mycaterer-new'), {
            'caterer_name': 'New Test Caterer',
            'caterer_description': 'New This is a test caterer',
            'location': 'Test Centre'
        })
        self.assertEqual(caterer_response.status_code, 302)
        self.assertTrue(Caterer.objects.filter(caterer_name='New Test Caterer').exists())

    def test_MyCatererUpdateView(self):
        self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        url = reverse('orders-mycaterer-update', kwargs={'pk': self.caterer.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'orders/myCaterer_form.html')

        self.assertEqual(self.caterer.caterer_name, 'Test Caterer')  # Check the original

        caterer_response = self.client.post(url, {
            'caterer_name': 'Update Test Caterer',
            'caterer_description': 'Update This is a test caterer',
            'location': 'Update Centre'
         })

        self.caterer.refresh_from_db()
        self.assertEqual(caterer_response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.caterer.caterer_name, 'Update Test Caterer')


    def test_MyCatererDeleteView(self):
        self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        url = reverse('orders-mycaterer-delete', kwargs={'pk': self.caterer.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'orders/myCaterer_confirm_delete.html')

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 302)  # Redirect after POST
        self.assertFalse(Caterer.objects.filter(pk=self.caterer.pk).exists())