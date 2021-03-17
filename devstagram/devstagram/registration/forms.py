from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from devstagram.mainsite.models import UserAuth


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    two_factor_auth = forms.ChoiceField(choices=(
        (True, 'YES'),
        (False, 'NO'),
    ))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','two_factor_auth']

    def clean(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username is already taken')

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user_auth = UserAuth(user=user, two_factor_auth=self.cleaned_data['two_factor_auth'])
        user.save()
        user_auth.save()
        return user