from django.conf import settings
from django.core.mail import send_mail
from nanoid import generate
from requests import get


# Create your classes here.


class TokenGenerator(object):
    tokens_storage = list()

    def __init__(self, account):
        self.token = generate(size=40).replace(' ', '-')
        self.account = account

    @classmethod
    def check_token(cls, account, token: str) -> bool:
        for token_obj in cls.tokens_storage:
            if token_obj.token == token and token_obj.account == account:
                cls.tokens_storage.remove(token_obj)
                return True
        return False

    @classmethod
    def make_token(cls, account) -> str:
        obj = TokenGenerator(account)
        cls.tokens_storage.append(obj)
        return obj.token


# Create your functions here
def send_remind(user, sity_id: int):
    key = settings.WEATHERBIT_KEY
    send_mail(
        subject='Weather Remind',
        message=get(
            f'https://api.weatherbit.io/v2.0/current?key={key}&city_id={sity_id}',
        ).content,
        from_email='nutmegraw@yandex.ru',
        recipient_list=[user.email],
        )
