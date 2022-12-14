from django.urls import path
from .views import RegPage, AuthPage, LogoutPage


urlpatterns = [
    path("reg/", RegPage.as_view(), name="reg"),
    path("auth/", AuthPage.as_view(), name="auth"),
    path("logout/", LogoutPage.as_view(), name="logout"),
]
