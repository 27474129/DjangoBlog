import logging
import json
from .models import Article
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger("debug")


class ArticleRepository:
    @staticmethod
    def get_article_by_slug(slug: int) -> Article or None:
        try:
            return Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_article_by_id(article_id: int) -> Article or None:
        article = Article.objects.filter(pk=article_id)
        return article[0] if len(article) != 0 else False
