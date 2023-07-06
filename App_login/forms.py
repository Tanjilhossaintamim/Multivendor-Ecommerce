from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Profile, Sellar


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class SellarForm(ModelForm):
    class Meta:
        model = Sellar
        exclude = ['user']
