import logging
from django.db.models import QuerySet
from .models import User


logger = logging.getLogger("debug")


class UserRepository:
    @staticmethod
    def get_user_by_email(email: str) -> User or None:
        user = User.objects.filter(email=email)
        return user[0] if len(user) != 0 else None

    @staticmethod
    def get_user_by_pk(pk: int) -> User or None:
        user = User.objects.filter(pk=pk)
        return user[0] if len(user) != 0 else None

    @staticmethod
    def check_is_user_already_exists(email: str) -> bool:
        return True if User.objects.filter(email=email).exists() else False

    @staticmethod
    def get_all() -> QuerySet:
        return User.objects.all()

    @staticmethod
    def delete_user(pk) -> User or None:
        user = UserRepository.get_user_by_pk(pk)
        if user is not None:
            user.delete()
            return user
        else:
            return None
