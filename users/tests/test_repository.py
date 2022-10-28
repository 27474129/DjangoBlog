import logging
from django.test import TestCase
from users.repository import UserRepository
from django.db.models import QuerySet
from users.models import User
from argon2 import PasswordHasher


logger = logging.getLogger("debug")


class UserRepositoryTest(TestCase):
    @staticmethod
    def hash(password: str) -> str:
        return PasswordHasher().hash(password)

    def test_get_user_by_email(self):
        email = "harlanvova525252@email.com"
        result = UserRepository.get_user_by_email(email=email)
        self.assertEqual(result, None)
        logger.debug(f"Tested: get_user_by_email(): with email: {email}; result: {result} ---OK")

        User.objects.create(
            firstname="Vladimir", secondname="Kharlan",
            email=email, password=self.hash("274741298")
        )
        result = UserRepository.get_user_by_email(email=email)
        self.assertEqual(type(result), User)
        logger.debug(f"Tested: get_user_by_email(): with email: {email}; result: {result} ---OK")

    def test_check_is_user_already_exists(self):
        email = "adsdasdasd@mail.com"
        result = UserRepository.check_is_user_already_exists(email=email)
        self.assertEqual(result, False)
        logger.debug(f"Tested: check_is_user_already_exists(): with email: {email}; result: {result} ---OK")

        User.objects.create(
            firstname="Vladimir", secondname="Kharlan",
            email=email, password=self.hash("274741298")
        )
        result = UserRepository.check_is_user_already_exists(email=email)
        self.assertEqual(result, True)
        logger.debug(f"Tested: check_is_user_already_exists(): with email: {email}; result: {result} ---OK")
