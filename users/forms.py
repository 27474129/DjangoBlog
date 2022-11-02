import re
import logging
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHash
from .repository import UserRepository
from .validators import UserValidators


logger = logging.getLogger("info")


class RegForm(forms.ModelForm):
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["firstname", "secondname", "email", "password"]
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_firstname(self):
        firstname = self.cleaned_data.get("firstname")
        errors = UserValidators.validate_firstname(firstname)
        if len(errors) != 0:
            raise ValidationError(errors)
        return firstname

    def clean_secondname(self):
        secondname = self.cleaned_data.get("secondname")
        errors = UserValidators.validate_secondname(secondname)
        if len(errors) != 0:
            raise ValidationError(errors)
        return secondname

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not UserValidators.validate_email(email):
            raise ValidationError("Email занят!")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        errors = UserValidators.validate_password(password)
        if len(errors) == 0:
            return PasswordHasher().hash(password)
        else:
            raise ValidationError(errors)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password is None:
            return password2
        try:
            logger.debug(password2)
            logger.debug(password)
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
