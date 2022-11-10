import logging
from django.test import TestCase
from users.forms import RegForm
from users.models import User
from django.db import connection
from users.validators import UserValidators


logger = logging.getLogger("debug")


class RegFormTestCase(TestCase):

    data = {
        'firstname': "Vladimir",
        'secondname': "Kharlan",
        'email': "harlanvova535@gmail.com",
        'password': "password253",
        'password2': "password253",
    }

    # Тест при котором не должно быть ошибок а простое прохождение валидации
    def test_reg_form_2(self):
        errors = UserValidators().execute_validators(self.data)
        self.assertEqual(len(errors), 0)
        logger.debug("test2: Tested: RegForm ---OK")

    # Тест при котором рейзиться ошибка "Email занят!"
    def test_reg_form_3(self):
        for i in range(2):
            User.objects.create(
                firstname=self.data["firstname"],
                secondname=self.data["secondname"],
                email=self.data["email"],
                password=self.data["password"],
            )
        errors = UserValidators().execute_validators(self.data)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0], "Email уже занят!")

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE users_user")
        logger.debug("test3: Tested: RegForm ---OK")

    # Тест при котором рейзятся ошибки: "Пароль должен содержать минимум одну цифру" и "Пароль должен содержать минимум 6 символов"
    def test_reg_form_4(self):
        previous_password = self.data["password"]
        self.data["password"] = "asd"
        errors = UserValidators().execute_validators(self.data)

        self.assertEqual(len(errors), 2)
        self.assertEqual("Пароль должен содержать минимум 6 символов", errors[0])
        self.assertEqual("Пароль должен содержать минимум одну цифру", errors[1])

        self.data["password"] = previous_password

        logger.debug("test4: Tested: RegForm ---OK")

    # Тест при котором рейзяться ошибки: Имя должно содержать только русские и/или английские буквы; Фамилия должна содержать только русские и/или английские буквы
    def test_reg_form_5(self):
        self.data["firstname"] = "52"
        self.data["secondname"] = "asdas2"
        self.data["password"] = "t3t3t3223t32"
        self.data["password2"] = "t3t3t3223t32"

        errors = UserValidators().execute_validators(self.data)

        self.assertEqual("Имя должно содержать только русские и/или английские буквы", errors[0])
        self.assertEqual("Фамилия должна содержать только русские и/или английские буквы", errors[1])
        self.assertEqual(len(errors), 2)

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE users_user")
        logger.debug("test5: Tested: RegForm ---OK")
