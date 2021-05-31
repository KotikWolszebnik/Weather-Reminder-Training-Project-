from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic


class RegistrationForm(UserCreationForm):
    @atomic
    def save(self, **kwargs):
        account = super(self.__class__, self).save(commit=False, **kwargs)
        account.username = account.email
        account.save()
        return account
