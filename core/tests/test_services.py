import logging
from django.test import TestCase
from core.forms import AddArticleForm
from random import randint
from core.services import AddArticlePageService
from api.tests.test_repository import ArticleCreation
from api.models import Mark, Comment
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger("debug")


class AddArticlePageServiceTest(TestCase, ArticleCreation):
    def test_validation_errors(self):
        form_data = {
            "title": "some title",
            "content": "some content",
            "who_uploaded": "albina",
            "slug": randint(1, 10000000),
        }
        form = AddArticleForm(data=form_data)

        errors = AddArticlePageService()._AddArticlePageService__get_validation_errors(form)
        parsed_errors = AddArticlePageService.parse_validation_errors(errors)
        logger.debug("Tested: validation_errors() ---OK")

    def test_allocate_space_for_marks_and_comments(self):
        new_article = super().create_new_article()
        AddArticlePageService._AddArticlePageService__allocate_space_for_marks(new_article)
        AddArticlePageService._AddArticlePageService__allocate_space_for_comments(new_article)

        try:
            Mark.objects.get(article=new_article.pk)
            self.assertTrue(True)
        except ObjectDoesNotExist:
            self.assertTrue(False)

        try:
            Comment.objects.get(article=new_article.pk)
            self.assertTrue(True)
        except ObjectDoesNotExist:
            self.assertTrue(False)

        logger.debug("Tested allocate_space_for_marks_and_comments() ---OK")
