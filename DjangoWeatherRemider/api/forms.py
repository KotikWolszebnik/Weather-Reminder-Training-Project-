from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic

from .models import User


class RegistrationForm(UserCreationForm):
    @atomic
    def save(self, **kwargs):
        account = super(self.__class__, self).save(commit=False, **kwargs)
        account.username = account.email
        account.save()
        return account

    class Meta(UserCreationForm):
        model = User
        fields = ('email', )
