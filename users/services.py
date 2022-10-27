import logging
from .repository import UsersRepository
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError


logger = logging.getLogger("debug")


class AuthPageService:
    @staticmethod
    def __check_data(entered_email: str, entered_password: str) -> bool:
        user = UsersRepository.get_user_by_email(entered_email)
        try:
            logger.info("checking data")
            logger.info("password from db: " + user.password)
            logger.info("entered password: " + entered_password)
            PasswordHasher().verify(user.password, entered_password)
            logger.info("passwords are the same")
            return True if entered_email == user.email else False
        except VerificationError:
            logger.info("Verification error")
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
            logger.info("authenticated")
            return True
        else:
            logger.info("incorrect username or password")
            return False
