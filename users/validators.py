import re
import logging
from django.core.exceptions import ValidationError
from django.http import QueryDict
from users.repository import UserRepository


logger = logging.getLogger("info")


class UserValidators:
    @staticmethod
    def get_letters_and_digits_count(value: str) -> list:
        result = []
        result.append(len(re.findall(r"[а-я]", value)))
        result.append(len(re.findall(r"[А-Я]", value)))
        result.append(len(re.findall(r"[a-z]", value)))
        result.append(len(re.findall(r"[A-Z]", value)))
        result.append(len(re.findall(r"[0-9]", value)))
        return result

    @staticmethod
    def validate_firstname(firstname: str) -> list:
        errors = []
        if len(firstname) < 2:
            errors.append("Имя должно содержать не менее 2х символов")

        letters_and_digits_count = UserValidators.get_letters_and_digits_count(firstname)

        if (
            letters_and_digits_count[0] + letters_and_digits_count[1] +
            letters_and_digits_count[2] + letters_and_digits_count[3] != len(firstname)
        ):
            errors.append("Имя должно содержать только русские и/или английские буквы")

        return errors

    @staticmethod
    def validate_secondname(secondname: str) -> list:
        errors = []
        if len(secondname) < 2:
            errors.append("Фамилия должна содержать не менее 2х символов")

        letters_and_digits_count = UserValidators.get_letters_and_digits_count(secondname)

        if (
                letters_and_digits_count[0] + letters_and_digits_count[1] +
                letters_and_digits_count[2] + letters_and_digits_count[3] != len(secondname)
        ):
            errors.append("Фамилия должна содержать только русские и/или английские буквы")

        return errors

    @staticmethod
    def validate_password(password: str) -> list:
        errors = []
        if len(password) < 6:
            errors.append("Пароль должен содержать минимум 6 символов")

        letters_and_digits_count = UserValidators.get_letters_and_digits_count(password)
        if letters_and_digits_count[-1] == 0:
            errors.append("Пароль должен содержать минимум одну цифру")

        return errors

    @staticmethod
    def validate_email(email: str) -> str or bool:
        return "Email уже занят!" if UserRepository.check_is_user_already_exists(email) else False

    def execute_validators(self, data: dict, mode="") -> list:
        errors = []
        for error in self.validate_firstname(data["firstname"]):
            errors.append(error)

        for error in self.validate_secondname(data["secondname"]):
            errors.append(error)

        if mode != "without_email_validation":
            email_validation_result = self.validate_email(data["email"])
            if type(email_validation_result) is str:
                errors.append(email_validation_result)

        for error in self.validate_password(data["password"]):
            errors.append(error)

        return errors
