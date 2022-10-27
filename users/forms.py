import re
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError


class RegForm(forms.ModelForm):
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["firstname", "secondname", "email", "password"]
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email занят!")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return PasswordHasher().hash(password)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        try:
            PasswordHasher().verify(password, password2)
        except VerificationError:
            raise ValidationError("Пароли не совпадают")
        return password2


class AuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]
        widgets = {
            "password": forms.PasswordInput,
        }

    #def clean_email(self):
        #email = self.cleaned_data.get("email")
        #password = self.cleaned_data.get("password")

