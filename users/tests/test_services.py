import logging
from django.test import TestCase
from users.services import AuthPageService
from users.models import User
from argon2 import PasswordHasher


logger = logging.getLogger("debug")


class RequestObjectImitation:
    def __init__(self, email, password):
        self.POST = {}
        self.POST["email"] = email
        self.POST["password"] = password


class AuthPageServiceTest(TestCase):
    @staticmethod
    def hash(password: str) -> str:
        return PasswordHasher().hash(password)

    def test_check_data(self):
        first_test_email = "harlanvova03@gmail.com"
        first_test_password = "27474129"
        second_test_email = "emailemail@main.com"
        second_test_password = "FSI8*АФgkfds"
        User.objects.create(
            firstname="Vladimir", secondname="Kharlan",
            email=first_test_email, password=self.hash(first_test_password)
        )
        result = AuthPageService._AuthPageService__check_data(first_test_email, first_test_password)
        self.assertTrue(result)
        logger.debug(f"Tested: check_data(): with email: {first_test_email}; with password: {first_test_password}; result: {result} ---OK")

        result = AuthPageService._AuthPageService__check_data(second_test_email, second_test_password)
        self.assertFalse(result)
        logger.debug(f"Tested: check_data(): with email: {second_test_email}; with password: {second_test_password}; result: {result} ---OK")

    def test_execute_service(self):
        email = "harlanvova03@gmail.com"
        password = "sdfsdsdsd"
        request = RequestObjectImitation(email=email, password=password)
        result = AuthPageService.execute_service(request)
        self.assertFalse(result)
        logger.debug(f"Tested: check_data(): with email: {email}; with password: {[password]}; result: {result} ---OK")
