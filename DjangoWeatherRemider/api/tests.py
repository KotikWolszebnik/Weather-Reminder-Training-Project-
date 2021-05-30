from django.core import mailcd
from django.test import TestCase
from django.utils.lorem_ipsum import words

from .models import City, Subscription, User


# Create your tests here.
class YourTestClass(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test@user.com',
            email='test@user.com',
            password='password',
        )

    def register_user(self):
        """Make the fixture."""
        resp = self.client.post(
            '/registration/',
            data=dict(
                email='test_user@test.com',
                first_name='Test',
                last_name='User',
                password1='kufkutfy764754dsdddddh',
                password2='kufkutfy764754dsdddddh',
            ),
            follow=True,
        )
        self.unique_token = str(mail.outbox[0].message())\
            .split('/confirm/')[1].split('/', maxsplit=1)[0]
        return resp

    def register_and_confirm(self):
        """Make the fixture."""
        self.register_user()
        return self.client.get(f'/confirm/{self.unique_token}/')

    def register_confirm_and_post(self):
        """Make the fixture."""
        resp = self.register_and_confirm()
        self.post_text = 'Присваивание в условии цикла - Python - Киберфорум'
        Post.objects.create(
            slug=1234567890,
            text=self.post_text,
            author=resp.wsgi_request.user)
        return self.client.get(f'/wall/{resp.wsgi_request.user.slug}/')

    def test_index_login_page(self):
        index_resp = str(self.client.get('/').content, encoding='utf-8')
        self.assertIn('<h5 class="card-title">Log in</h5>', index_resp)