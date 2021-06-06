from django.core import mail
from django.test import TestCase

from .models import City, Subscription


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
            '/api/v1/register/',
            data=dict(
                email='test@user.com',
                password='kufkutfy764754dsdddddh',
            ),
            follow=True,
        )
        self.unique_token = str(mail.outbox[0].message())\
            .split('/confirm/')[1].split('/', maxsplit=1)[0]
        return resp

    def register_and_get_jwt(self):
        """Make the fixture."""
        self.register_user()  # fixture

        resp = self.client.post(
            '/api/v1/token/',
            data=dict(
                email='test@user.com',
                password='kufkutfy764754dsdddddh',
            ),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.refresh = resp_str.split('"refresh":"')[1].split('"')[0]
        self.access = resp_str.split('"access":"')[1].split('"')[0]
        return resp

    def reg_confirm(self):
        self.register_and_get_jwt()  # fixture

        resp = self.client.get(
            f'/api/v1/confirm/{self.unique_token}/',
            follow=True,
            HTTP_AUTHORIZATION='Bearer ' + self.access,
        )
        return resp

    def reg_confirm_make_subscription(self):
        self.reg_confirm()  # fixture

        resp = self.client.post(
            '/api/v1/subscription/',
            data=dict(
                city=709930,
                notification_period=3,
            ),
            follow=True,
            HTTP_AUTHORIZATION='Bearer ' + self.access,
        )
        return resp

    def test_registration(self):
        resp = self.register_user()  # fixture

        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('"password":"pbkdf2_sha', resp_str)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

    def test_jwt_getting(self):
        resp = self.register_and_get_jwt()  # fixture

        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('"refresh":', resp_str)
        self.assertIn('"access":', resp_str)

    def test_reg_confirm(self):
        resp = self.reg_confirm()  # fixture

        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn("You've got confirming success.", resp_str)

    def test_sities_listing(self):
        self.reg_confirm()  # fixture

        resp = self.client.get(
            '/api/v1/city/search_by_name/',
            data=dict(name='Kiev'),
            follow=True,
            HTTP_AUTHORIZATION='Bearer ' + self.access,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn("Ukraine", resp_str)
        self.assertNotIn('Russia', resp_str)

    def test_subscription_creating(self):
        resp = self.reg_confirm()  # fixture
        before = len(list(resp.wsgi_request.user.subscriptions.all()))

        resp = self.reg_confirm_make_subscription()  # fixture
        after = len(list(resp.wsgi_request.user.subscriptions.all()))

        self.assertEqual(after - before, 1)

        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('{"id":1,"notification_period":3,"city":709930}', resp_str)

    def test_subscriptions_listing(self):
        resp = self.reg_confirm()  # fixture
        Subscription(
            user=resp.wsgi_request.user,
            city=City.objects.get(id=703448),
            notification_period=1,
        ).save()  # fixture
        Subscription(
            user=resp.wsgi_request.user,
            city=City.objects.get(id=1486209),
            notification_period=24,
        ).save()  # fixture

        resp = self.client.get(
            '/api/v1/subscription/all/',
            follow=True,
            HTTP_AUTHORIZATION='Bearer ' + self.access,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(
            '[{"id":3,"notification_period":24,"city":1486209},{"id":2,"notification_period":1,"city":703448}]',
            resp_str,
            )

    def test_subscriptions_update(self):
        resp = self.reg_confirm_make_subscription()  # fixture

        before = resp.wsgi_request.user.subscriptions.filter(
            city=City.objects.get(id=709930), notification_period=24,
            ).exists()
        self.assertFalse(before)

        resp = self.client.put(
            '/api/v1/subscription/4/',
            data=dict(notification_period=24),
            content_type='application/json',
            follow=True,
            HTTP_AUTHORIZATION='Bearer ' + self.access,
        )

        after = resp.wsgi_request.user.subscriptions.filter(
            city=City.objects.get(id=709930), notification_period=24,
            ).exists()
        self.assertTrue(after)

        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('{"id":4,"notification_period":24,"city":709930}', resp_str)

    def test_subscriptions_vdestroy(self):
        resp = self.reg_confirm_make_subscription()  # fixture

        before = resp.wsgi_request.user.subscriptions.filter(
            city=City.objects.get(id=709930), notification_period=3,
            ).exists()
        self.assertTrue(before)

        resp = self.client.delete(
            '/api/v1/subscription/5/',
            content_type='application/json',
            follow=True,
            HTTP_AUTHORIZATION='Bearer ' + self.access,
        )

        after = resp.wsgi_request.user.subscriptions.filter(
            city=City.objects.get(id=709930), notification_period=3,
            ).exists()
        self.assertFalse(after)
