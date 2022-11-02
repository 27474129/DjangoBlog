import logging
from random import randint
from django.test import TestCase
from core.services import AddArticlePageService
from core.models import Article
from django.db.models import QuerySet
from api.repository import MarkRepository, CommentRepository
from api.models import Mark, Comment
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger("debug")


class ArticleCreation:
    @staticmethod
    def create_new_article() -> Article:
        return Article.objects.create(
            title="some title",
            content="some content",
            photo="plut",
            slug=randint(1, 999999999999999),
            is_published=True
        )


class MarkRepositoryTest(TestCase, ArticleCreation):
    def test_get_mark_by_id(self):
        new_article = super().create_new_article()
        AddArticlePageService._AddArticlePageService__allocate_space_for_marks(new_article)

        article_marks, articles_marks = MarkRepository.get_mark_by_id(new_article.pk)
        self.assertEqual(type(article_marks), Mark)
        self.assertEqual(type(articles_marks), QuerySet)

        self.assertEqual(MarkRepository.get_mark_by_id(532523), None)
        logger.debug("Tested get_mark_by_id() ---OK")

    def test_allocate_space_for_marks(self):
        new_article = super().create_new_article()
        MarkRepository.allocate_space_for_marks(new_article)

        try:
            Mark.objects.get(article=new_article.pk)
            self.assertTrue(True)
        except ObjectDoesNotExist:
            logger.debug("Tested allocate_space_for_marks(): Marks was not created")
            self.assertTrue(False)

        logger.debug("Tested allocate_space_for_marks() ---OK")


class CommentRepositoryTest(TestCase, ArticleCreation):
    def test_get_comments_by_article_id(self):
        new_article = super().create_new_article()
        AddArticlePageService._AddArticlePageService__allocate_space_for_comments(new_article)
        article_comments, articles_comments = CommentRepository.get_comments_by_article_id(new_article.pk)
        self.assertEqual(type(article_comments), Comment)
        self.assertEqual(type(articles_comments), QuerySet)

        self.assertEqual(CommentRepository.get_comments_by_article_id(52525252), None)

        logger.debug("Tested get_comments_by_article_id() ---OK")

    def test_allocate_space_for_comments(self):
        new_article = super().create_new_article()
        AddArticlePageService._AddArticlePageService__allocate_space_for_comments(new_article)

        try:
            Comment.objects.get(article=new_article.pk)
            self.assertTrue(True)
        except ObjectDoesNotExist:
            logger.debug("Tested allocate_space_for_comments(): Comments was not created")
            self.assertTrue(False)

        logger.debug("Tested allocate_space_for_comments() ---OK")
