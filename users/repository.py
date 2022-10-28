import logging
from .models import User
from django.db.models import QuerySet


logger = logging.getLogger("debug")


class UserRepository:
    @staticmethod
    def get_user_by_email(email: str) -> User or None:
        user = User.objects.filter(email=email)
        return user[0] if len(user) != 0 else None

    @staticmethod
    def check_is_user_already_exists(email: str) -> bool:
        return True if User.objects.filter(email=email).exists() else False
