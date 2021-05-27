from django.http import HttpResponseNotAllowed
from nanoid import generate
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, UpdateModelMixin)


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


class CLUDAPIView(
    GenericAPIView, CreateModelMixin, DestroyModelMixin,
    ListModelMixin, UpdateModelMixin,
):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Create your decorators here.


def post_method_required(func):
    """Decoraror"""
    def wrapper(request):
        if request.method == 'POST':
            return func(request)
        return HttpResponseNotAllowed(['POST'])
    return wrapper

