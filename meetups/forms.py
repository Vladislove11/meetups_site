from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Meetup


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Ваш Email")

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Имя пользователя",
            "email": "Email",
            "password": "Пароль",
            "password2": "Подтверждение пароля"
        }
        help_text = {
            "username": "Обязательное поле. До 150 символов. Только буквы и цифры и @/./+/-/_."
        }

class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = ["title", "slug", "description", "image", "date", "location", "organizer_email"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)