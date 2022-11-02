import logging
import json
from random import randint
from .forms import AddArticleForm
from api.repository import CommentRepository, MarkRepository
from .repository import ArticleRepository
from django.db.models import QuerySet
from .models import Article
from api.models import Mark


logger = logging.getLogger("info")


class AddArticlePageService:
    def __check_form_data(self, request) -> list:
        form_data = {
            "title": request.POST["title"],
            "content": request.POST["content"],
            "who_uploaded": "albina",
            "slug": randint(1, 10000000),
        }
        form = AddArticleForm(form_data, request.FILES)
        logger.debug(form.errors)
        return [form, True] if form.is_valid() else [form, False]

    def __save_form(self, form: AddArticleForm) -> Article:
        return form.save()

    def __get_validation_errors(self, form: AddArticleForm) -> str:
        errors = ""
        logger.info(form.errors)
        for field in form.errors:
            for error in form.errors[field]:
                errors += error + ";"

        return errors

    @staticmethod
    def __allocate_space_for_marks(article_instance: Article) -> None:
        MarkRepository.allocate_space_for_marks(article_instance)

    @staticmethod
    def __allocate_space_for_comments(article_instance: Article) -> None:
        CommentRepository.allocate_space_for_comments(article_instance)

    @staticmethod
    def parse_validation_errors(errors) -> list:
        parsed_errors = errors.split(";")
        parsed_errors.remove("")
        return parsed_errors

    def execute_service(self, request) -> None or str:
        form, is_valid = self.__check_form_data(request)
        if is_valid:
            article_instance = self.__save_form(form)
            self.__allocate_space_for_marks(article_instance)
            self.__allocate_space_for_comments(article_instance)
        else:
            return self.__get_validation_errors(form)
