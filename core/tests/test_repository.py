import logging
from django.test import TestCase
from core.models import Article
from core.repository import ArticleRepository
from random import randint
from django.db.models import QuerySet
from core.services import AddArticlePageService
from django.core.exceptions import ObjectDoesNotExist
from api.tests.test_repository import ArticleCreation


logger = logging.getLogger("debug")


class ArticleRepositoryTest(TestCase, ArticleCreation):
    def test_get_article_by_slug(self):

        new_article = super().create_new_article()
        article = ArticleRepository.get_article_by_slug(new_article.slug)
        self.assertEqual(type(article), Article)

        article = ArticleRepository.get_article_by_slug(1)
        self.assertEqual(article, None)

        logger.debug("Tested get_article_by_slug() ---OK")
