from .models import User
from django.db.models import QuerySet


class UsersRepository:
    @staticmethod
    def get_user_by_email(email) -> QuerySet or None:
        user = User.objects.filter(email=email)
        return user[0] if len(user) != 0 else None
