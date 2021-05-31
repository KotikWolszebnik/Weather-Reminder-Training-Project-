from django.core import mail
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import City, Subscription, User


# Create your tests here.
class YourTestClass(TestCase):

    def setUp(self):
        # Make a little fixture with cities
        cities_list = [
            dict(id=524901, name='Moscow', state_code='48',country='Russia', country_code='RU'),
            dict(id=703448, name='Kiev', state_code='12', country='Ukraine', country_code='UA'),
            dict(id=1486209, name='Yekaterinburg', state_code='71', country='Russia', country_code='RU'),
            dict(id=709930, name='Dnipro', state_code='04', country='Ukraine', country_code='UA'),
        ]
        for city in cities_list:
            obj = City(
                id=city['id'],
                name=city['name'],
                state_code=city['state_code'],
                country=city['country'],
                country_code=city['country_code'],
            )
            obj.save()
    
    def register_user(self):
        """Make the fixture."""
        resp = self.client.post(
            '/registration/',
            data=dict(
                username='test_user@test.com',
                email='test_user@test.com',
                password1='kufkutfy764754dsdddddh',
                password2='kufkutfy764754dsdddddh',
            ),
            follow=True,
        )
        print(resp)
        self.unique_token = str(mail.outbox[0].message())\
            .split('/confirm/')[1].split('/', maxsplit=1)[0]
        return resp

    def register_and_confirm(self):
        """Make the fixture."""
        self.register_user()
        return self.client.get(f'/confirm/{self.unique_token}/')

    def test_registration(self):
        resp = self.register_user()  # fixture

        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('200', resp_str)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

    def test_reg_confirm(self):
        pass

    def test_jwt_getting(self):
        pass

    def test_sities_listing(self):
        pass

    def test_subscription_creating(self):
        pass

    def test_subscriptions_listing(self):
        pass

    def test_subscriptions_update(self):
        pass

    def test_subscriptions_destroy(self):
        pass

