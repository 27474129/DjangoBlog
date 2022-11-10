import logging
from django.urls import reverse
from django.test import TestCase
from blognews import settings
from core.models import Article
from random import randint
from .test_repository import ArticleCreation


logger = logging.getLogger("debug")


class CoreViewsTest(TestCase, ArticleCreation):
    def test_index_page(self):
        response = self.client.get(reverse("index"))
        logger.debug(f"GET request to url: {settings.ALLOWED_HOSTS[0]}:8000{reverse('index')}")
        self.assertEqual(response.status_code, 200)
        logger.debug("Tested: IndexPage: ---OK")

    def test_add_article_page(self):
        response = self.client.get(reverse("addarticle"))
        logger.debug(f"GET request to url: {settings.ALLOWED_HOSTS[0]}:8000{reverse('addarticle')}")
        self.assertEqual(response.status_code, 200)
        logger.debug("Tested: AddArticlePage: ---OK")

    def test_article_page(self):
        new_article = super().create_new_article()
        response = self.client.get(reverse("article") + str(new_article.slug))
        logger.debug(f"GET request to url: {settings.ALLOWED_HOSTS[0]}:8000{reverse('article')}{new_article.slug}")
        self.assertEqual(response.status_code, 200)
        logger.debug("Tested: ArticlePage: ---OK")

        response = self.client.get(reverse("article"))
        logger.debug("GET request to url: " + reverse("article"))
        self.assertEqual(response.status_code, 404)
        logger.debug("Tested: article_url_plut: ---OK")
