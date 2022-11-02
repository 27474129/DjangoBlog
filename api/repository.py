import json
from django.db.models import QuerySet
from core.models import Article
from django.core.exceptions import ObjectDoesNotExist
from .models import Mark, Comment


class MarkRepository:
    @staticmethod
    def get_mark_by_id(article_id: int) -> list or None:
        articles_marks = Mark.objects.filter(article=article_id)
        if len(articles_marks) == 0:
            return None
        article_marks = articles_marks[0]
        return [article_marks, articles_marks]

    @staticmethod
    def allocate_space_for_marks(article_instance: Article) -> None:
        Mark.objects.create(article=article_instance, users_liked=json.dumps({"liked": []}), \
                            users_disliked=json.dumps({"disliked": []}))


class CommentRepository:
    @staticmethod
    def get_comments_by_article_id(article_id: int) -> list or None:
        articles_comments = Comment.objects.filter(article=article_id)
        if len(articles_comments) == 0:
            return None
        article_comments = articles_comments[0]
        return [article_comments, articles_comments]

    @staticmethod
    def allocate_space_for_comments(article_instance: Article) -> None:
        Comment.objects.create(article=article_instance, comments=json.dumps({}))
