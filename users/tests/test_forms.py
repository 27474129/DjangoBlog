import logging
from django.test import TestCase
from users.forms import RegForm
from users.models import User


logger = logging.getLogger("debug")


class RegFormTestCase(TestCase):

    data = {
        'firstname': "Vladimir",
        'secondname': "Kharlan",
        'email': "harlanvova535@gmail.com",
        'password': "password253",
        'password2': "password253",
    }

    # Тест при котором должна рейзиться ошибка "Пароли не сопадаю"
    def test_reg_form_1(self):
        self.data["password2"] = "asdsadaad"
        form = RegForm(data=self.data)

        errors = []
        for field in form.errors:
            for error in form.errors[field]:
                errors.append(error)

        self.assertEqual(errors[0], "Пароли не совпадают")
        self.assertEqual(len(errors), 1)
        logger.debug("test1: Tested: RegForm ---OK")

    # Тест при котором не должно быть ошибок а простое прохождение валидации
    def test_reg_form_2(self):
        self.data["password2"] = self.data["password"]
        form = RegForm(data=self.data)

        errors = []
        for field in form.errors:
            for error in form.errors[field]:
                errors.append(error)

        self.assertEqual(len(errors), 0)
        logger.debug("test2: Tested: RegForm ---OK")

    # Тест при котором рейзиться ошибка "Email занят!"
    def test_reg_form_3(self):
        self.data["password2"] = self.data["password"]
        User.objects.create(
            firstname=self.data["firstname"],
            secondname=self.data["secondname"],
            email=self.data["email"],
            password=self.data["password"],
        )

        form = RegForm(data=self.data)

        errors = []
        for field in form.errors:
            for error in form.errors[field]:
                errors.append(error)

        self.assertEqual(len(errors), 1)
        self.assertEqual("Email занят!", errors[0])
        logger.debug("test3: Tested: RegForm ---OK")

    # Тест при котором рейзиться ошибка "Пароли не совпадают" и "Пароль должен содержать минимум одну цифру" и "Пароль должен содержать минимум 6 символов"
    def test_reg_form_4(self):
        self.data["password"] = "asd"

        form = RegForm(data=self.data)

        errors = []
        for field in form.errors:
            for error in form.errors[field]:
                errors.append(error)

        logger.debug(errors)
