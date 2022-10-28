import logging
from .repository import UserRepository
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash

logger = logging.getLogger("info")


class AuthPageService:
    @staticmethod
    def __check_data(entered_email: str, entered_password: str) -> bool:
        user = UserRepository.get_user_by_email(entered_email)
        if user is None:
            return False
        try:
            PasswordHasher().verify(user.password, entered_password)
            return True if entered_email == user.email else False
        except InvalidHash:
            return False

    @staticmethod
    def __authenticate(request, email: str) -> None:
        request.session.set_expiry(1296000)
        request.session["email"] = email

    @staticmethod
    def execute_service(request) -> bool:
        entered_email = request.POST["email"]
        entered_password = request.POST["password"]
        if AuthPageService.__check_data(entered_email, entered_password):
            AuthPageService.__authenticate(request, entered_email)
            logger.debug("authenticated")
            return True
        else:
            logger.debug("incorrect username or password")
            return False
