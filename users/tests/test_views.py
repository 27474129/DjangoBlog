import logging
from django.urls import reverse
from django.test import TestCase
from blognews import settings


logger = logging.getLogger("debug")


class UsersViewsTest(TestCase):
    def test_reg_page(self):
        response = self.client.get(reverse("reg"))
        logger.debug(f"GET request to url: {settings.ALLOWED_HOSTS[0]}:8000{reverse('reg')}")
        self.assertEqual(response.status_code, 200)
        logger.debug("Tested: RegPage: ---OK")

    def test_auth_page(self):
        response = self.client.get(reverse("auth"))
        logger.debug(f"GET request to url: {settings.ALLOWED_HOSTS[0]}:8000{reverse('auth')}")
        self.assertEqual(response.status_code, 200)
        logger.debug("Tested: AuthPage: ---OK")

    def test_logout_page(self):
        response = self.client.get(reverse("logout"))
        logger.debug(f"GET request to url: {settings.ALLOWED_HOSTS[0]}:8000{reverse('logout')}")
        logger.debug(response.status_code)
        self.assertEqual(response.status_code, 302)
        logger.debug("Tested: LogoutPage: ---OK")
