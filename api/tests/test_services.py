import logging
from django.test import TestCase
from api.services import Serializing, UserMarkService
from core.forms import AddArticleForm
from api.tests.test_repository import ArticleCreation
from api.repository import MarkRepository, CommentRepository
from core.models import Article


logger = logging.getLogger("debug")


class SerializingTest(TestCase):
    def test_serialize(self):
        result = Serializing.serialize({"key": "value"})
        self.assertEqual(type(result), str)
        logger.debug("serialize() method is ---OK")

    def test_deserialize(self):
        json = Serializing.serialize({"key": "value"})
        result = Serializing.deserialize(json)
        self.assertEqual(type(result), dict)
        logger.debug("deserialize() method is ---OK")


class UserMarkServiceTest(TestCase, ArticleCreation):
    email = "harlanvova03@gmail.com"

    def __set_mark(self, article_id, mark):
        UserMarkService(
            article_id=article_id,
            user_email=self.email,
            mark=mark
        ).execute()

    def test_get_likes_dislikes_count(self):
        new_article = super().create_new_article()

        MarkRepository.allocate_space_for_marks(new_article)

        self.__set_mark(article_id=new_article.pk, mark="like")

        likes, dislikes = UserMarkService.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 1})
        self.assertEqual(dislikes, {new_article.pk: 0})
        logger.debug("Tested: get_likes_dislikes_count() ---OK")

    def test_add_delete_like(self):
        new_article = super().create_new_article()
        MarkRepository.allocate_space_for_marks(new_article)

        # тест1
        user_mark_service = UserMarkService(
            article_id=new_article.pk,
            user_email="harlanvova03@gmail.com",
            mark="like",
            mode="add"
        )
        user_mark_service._UserMarkService__add_delete_like()

        likes, dislikes = user_mark_service.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 1})
        self.assertEqual(dislikes, {new_article.pk: 0})

        # тест2
        user_mark_service = UserMarkService(
            article_id=new_article.pk,
            user_email="harlanvova15@gmail.com",
            mark="like",
            mode="add"
        )
        user_mark_service._UserMarkService__add_delete_like()

        likes, dislikes = user_mark_service.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 2})
        self.assertEqual(dislikes, {new_article.pk: 0})

        # тест3
        user_mark_service = UserMarkService(
            article_id=new_article.pk,
            user_email="harlanvova03@gmail.com",
            mark="like",
            mode="delete"
        )
        user_mark_service._UserMarkService__add_delete_like()

        likes, dislikes = user_mark_service.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 1})
        self.assertEqual(dislikes, {new_article.pk: 0})

        logger.debug("Tested add_delete_like() ---OK")

    def test_add_delete_dislike(self):
        new_article = super().create_new_article()
        MarkRepository.allocate_space_for_marks(new_article)

        # тест1
        user_mark_service = UserMarkService(
            article_id=new_article.pk,
            user_email="harlanvova03@gmail.com",
            mark="dislike",
            mode="add"
        )

        user_mark_service._UserMarkService__add_delete_dislike()

        likes, dislikes = user_mark_service.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 0})
        self.assertEqual(dislikes, {new_article.pk: 1})

        # тест2
        user_mark_service = UserMarkService(
            article_id=new_article.pk,
            user_email="harlanvova15@gmail.com",
            mark="dislike",
            mode="add"
        )
        user_mark_service._UserMarkService__add_delete_dislike()

        likes, dislikes = user_mark_service.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 0})
        self.assertEqual(dislikes, {new_article.pk: 2})

        # тест3
        user_mark_service = UserMarkService(
            article_id=new_article.pk,
            user_email="harlanvova03@gmail.com",
            mark="dislike",
            mode="delete"
        )
        user_mark_service._UserMarkService__add_delete_dislike()

        likes, dislikes = user_mark_service.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 0})
        self.assertEqual(dislikes, {new_article.pk: 1})

        logger.debug("Tested add_delete_dislike() ---OK")

    def test_get_user_mark_status(self):
        new_article = super().create_new_article()
        MarkRepository.allocate_space_for_marks(new_article)

        # тест1
        user_mark_service = UserMarkService(
            article_id=new_article.pk,
            user_email="harlanvova03@gmail.com",
            mark="like",
            mode="add"
        )

        result = user_mark_service._UserMarkService__get_user_mark_status()
        self.assertEqual(result, None)

        # тест2
        self.__set_mark(article_id=new_article.pk, mark="like")

        result = user_mark_service._UserMarkService__get_user_mark_status()

        self.assertEqual(result, "liked")

        #тест3
        self.__set_mark(article_id=new_article.pk, mark="dislike")

        result = user_mark_service._UserMarkService__get_user_mark_status()

        self.assertEqual(result, "disliked")

        logger.debug("Tested get_user_mark_status() ---OK")

    # общая функция которая тестирует сам функционал добавления и удаления лайков
    def test_functional(self):
        new_article = super().create_new_article()

        MarkRepository.allocate_space_for_marks(new_article)

        # тест1
        self.__set_mark(article_id=new_article.pk, mark="dislike")

        likes, dislikes = UserMarkService.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 0})
        self.assertEqual(dislikes, {new_article.pk: 1})

        # тест2
        self.__set_mark(article_id=new_article.pk, mark="dislike")

        likes, dislikes = UserMarkService.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 0})
        self.assertEqual(dislikes, {new_article.pk: 0})

        # тест3
        self.__set_mark(article_id=new_article.pk, mark="dislike")
        self.__set_mark(article_id=new_article.pk, mark="like")

        likes, dislikes = UserMarkService.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 1})
        self.assertEqual(dislikes, {new_article.pk: 0})

        # тест4
        self.__set_mark(article_id=new_article.pk, mark="dislike")

        likes, dislikes = UserMarkService.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 0})
        self.assertEqual(dislikes, {new_article.pk: 1})

        # тест5
        previous_email = self.email
        self.email = "harlanvakfka@fjgsd.com"
        self.__set_mark(article_id=new_article.pk, mark="dislike")
        self.email = previous_email

        likes, dislikes = UserMarkService.get_likes_dislikes_count()

        self.assertEqual(likes, {new_article.pk: 0})
        self.assertEqual(dislikes, {new_article.pk: 2})

        logger.debug("Tested functional ---OK")
