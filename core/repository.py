import logging
import json
from .models import Article, Mark, Comment
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger("debug")


class ArticleMarkRepository:
    @staticmethod
    def get_article_by_slug(slug: int) -> QuerySet or None:
        try:
            return Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_mark_by_id(article_id: int) -> list:
        articles_marks = Mark.objects.filter(article=article_id)
        article_marks = articles_marks[0]
        return [article_marks, articles_marks]

    @staticmethod
    def allocate_space_for_marks(article_instance: QuerySet) -> None:
        Mark.objects.create(article=article_instance, users_liked=json.dumps({"liked": []}), \
                            users_disliked=json.dumps({"disliked": []}))


class CommentRepository:
    @staticmethod
    def get_comments_by_article_id(article_id: int) -> list:
        articles_comments = Comment.objects.filter(article=article_id)
        article_comments = articles_comments[0]
        return [article_comments, articles_comments]

    @staticmethod
    def allocate_space_for_comments(article_instance: QuerySet) -> None:
        Comment.objects.create(article=article_instance, comments=json.dumps({}))