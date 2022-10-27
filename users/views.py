import logging
from django.shortcuts import render
from django.views.generic import CreateView, FormView
from core.views import BaseView
from .forms import RegForm, AuthForm
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from .repository import UsersRepository
from .models import User
from .services import AuthPageService
from django.contrib.auth.views import LogoutView


logger = logging.getLogger("debug")


class RegPage(BaseView, CreateView):
    template_name = "users/regpage.html"
    form_class = RegForm
    success_url = reverse_lazy("auth")


class AuthPage(BaseView, FormView):
    template_name = "users/authpage.html"
    form_class = AuthForm
    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        AuthPageService.execute_service(request)
        return super().post(request, *args, **kwargs)


class LogoutPage(LogoutView):
    next_page = reverse_lazy("index")
