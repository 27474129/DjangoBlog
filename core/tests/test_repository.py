import logging
from django.test import TestCase
from core.models import Article, Mark, Comment
from random import randint
from core.repository import ArticleMarkRepository, CommentRepository
from django.db.models import QuerySet
from core.services import AddArticlePageService
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


class ArticleMarkRepositoryTest(TestCase, ArticleCreation):
    def test_get_article_by_slug(self):

        new_article = super().create_new_article()
        article = ArticleMarkRepository.get_article_by_slug(new_article.slug)
        self.assertEqual(type(article), Article)

        article = ArticleMarkRepository.get_article_by_slug(1)
        self.assertEqual(article, None)

        logger.debug("Tested get_article_by_slug() ---OK")

    def test_get_mark_by_id(self):
        new_article = super().create_new_article()
        AddArticlePageService._AddArticlePageService__allocate_space_for_marks(new_article)

        article_marks, articles_marks = ArticleMarkRepository.get_mark_by_id(new_article.pk)
        self.assertEqual(type(article_marks), Mark)
        self.assertEqual(type(articles_marks), QuerySet)

        self.assertEqual(ArticleMarkRepository.get_mark_by_id(532523), None)
        logger.debug("Tested get_mark_by_id() ---OK")

    def test_allocate_space_for_marks(self):
        new_article = super().create_new_article()
        ArticleMarkRepository.allocate_space_for_marks(new_article)

        try:
            Mark.objects.get(pk=new_article.pk)
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
