import re
from django.core.exceptions import ValidationError


class UserValidators:
    @staticmethod
    def get_letters_and_digits_count(value):
        result = []
        result.append(len(re.findall(r"[а-я]", value)))
        result.append(len(re.findall(r"[А-Я]", value)))
        result.append(len(re.findall(r"[a-z]", value)))
        result.append(len(re.findall(r"[A-Z]", value)))
        result.append(len(re.findall(r"[0-9]", value)))
        return result

    @staticmethod
    def validate_firstname(firstname):
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
    def validate_secondname(secondname):
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
    def validate_password(password):
        errors = []
        if len(password) < 6:
            errors.append("Пароль должен содержать минимум 6 символов")

        letters_and_digits_count = UserValidators.get_letters_and_digits_count(password)
        if letters_and_digits_count[-1] == 0:
            errors.append("Пароль должен содержать минимум одну цифру")

        return errors
