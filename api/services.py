import logging
import json
from random import randint
from .repository import MarkRepository, CommentRepository
from django.db.models import QuerySet
from .models import Mark
from core.models import Article
from .serializers import UserSerializer
from users.validators import UserValidators


logger = logging.getLogger("info")


class Serializing:
    @staticmethod
    def serialize(object) -> str:
        return json.dumps(object)

    @staticmethod
    def deserialize(object) -> dict or list:
        return json.loads(object)


class UserMarkService(Serializing):
    def __init__(
            self,
            article_id: int,
            user_email: str,
            mark: str,
            mode=""
    ):
        self.__article_id = article_id
        self.__user_email = user_email
        self.__new_mark = mark
        self.__mode = mode

    @staticmethod
    def get_likes_dislikes_count() -> list:
        likes = {}
        dislikes = {}
        marks = Mark.objects.all()
        for mark in marks:
            likes[mark.article_id] = len(UserMarkService.deserialize(mark.users_liked)["liked"])
            dislikes[mark.article_id] = len(UserMarkService.deserialize(mark.users_disliked)["disliked"])
        return [likes, dislikes]

    def __add_delete_like(self) -> None or False:
        article_likes_list, articles_likes_list = MarkRepository.get_mark_by_id(self.__article_id)
        new_users_who_liked = {"liked": UserMarkService.deserialize(article_likes_list.users_liked)["liked"]}
        if self.__mode == "add":
            new_users_who_liked["liked"].append(self.__user_email)
        elif self.__mode == "delete":
            new_users_who_liked["liked"].remove(self.__user_email)
        else:
            return None
        articles_likes_list.update(users_liked=UserMarkService.serialize(new_users_who_liked))

    def __add_delete_dislike(self) -> None or False:
        article_dislikes_list, articles_dislikes_list = MarkRepository.get_mark_by_id(self.__article_id)
        new_users_who_disliked = {"disliked": UserMarkService.deserialize(article_dislikes_list.users_disliked)["disliked"]}
        if self.__mode == "add":
            new_users_who_disliked["disliked"].append(self.__user_email)
        elif self.__mode == "delete":
            new_users_who_disliked["disliked"].remove(self.__user_email)
        else:
            return None
        articles_dislikes_list.update(users_disliked=UserMarkService.serialize(new_users_who_disliked))

    def __get_user_mark_status(self) -> str or None or bool:
        marks, garbage = MarkRepository.get_mark_by_id(self.__article_id)
        users_who_liked = UserMarkService.deserialize(marks.users_liked)["liked"]
        users_who_disliked = UserMarkService.deserialize(marks.users_disliked)["disliked"]
        if self.__user_email in users_who_liked:
            return "liked"
        elif self.__user_email in users_who_disliked:
            return "disliked"

    def __set_mode_and_change_mark_status(self, current_mark: str or None) -> None:
        logger.debug(current_mark)
        if current_mark == "liked":
            logger.debug("new mark: like")
            if self.__new_mark == "like":
                logger.debug("new mark: like")
                self.__mode = "delete"
                self.__add_delete_like()
            else:
                logger.debug("new mark: dislike")
                self.__mode = "delete"
                self.__add_delete_like()
                self.__mode = "add"
                self.__add_delete_dislike()
        elif current_mark == "disliked":
            logger.debug("current mark: disliked")
            if self.__new_mark == "dislike":
                logger.debug("new mark: dislike")
                self.__mode = "delete"
                self.__add_delete_dislike()
            else:
                logger.debug("new mark: like")
                self.__mode = "delete"
                self.__add_delete_dislike()
                self.__mode = "add"
                self.__add_delete_like()
        else:
            self.__mode = "add"
            if self.__new_mark == "like":
                logger.debug("new mark: like")
                self.__add_delete_like()
            else:
                logger.debug("new mark: dislike")
                self.__add_delete_dislike()

    def execute(self):
        self.__set_mode_and_change_mark_status(current_mark=self.__get_user_mark_status())


class UserCommentService(Serializing):
    def __init__(
            self,
            article_id: int,
            user_email: str,
            comment: str,
    ):
        self.__article_id = article_id
        self.__email = user_email
        self.__comment = comment

    @staticmethod
    def get_comments(article_id: int):
        pass

    def __validate_comment(self) -> bool:
        return True if "fuck" not in self.__comment else False

    def __add_comment(self) -> None:
        article_comments, articles_comments = CommentRepository.get_comments_by_article_id(self.__article_id)
        comments = UserCommentService.deserialize(article_comments.comments)
        comments[self.__email] = self.__comment
        logger.info(comments)
        articles_comments.update(comments=UserCommentService.serialize(comments))

    def execute(self) -> bool:
        if self.__validate_comment():
            self.__add_comment()
            return True
        else:
            return False


class UserAPIService:
    @staticmethod
    def post(request) -> list:
        serializer = UserSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        errors = UserValidators().execute_validators(data=request.query_params)
        if len(errors) == 0:
            serializer.save()
            return [True, serializer.data]
        else:
            return [False, errors]
