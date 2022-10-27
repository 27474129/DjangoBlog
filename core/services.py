import logging
import json
from random import randint
from .forms import AddArticleForm
from .repository import ArticleMarkRepository, CommentRepository
from django.db.models import QuerySet
from core.models import Mark


logger = logging.getLogger("debug")


class Serializing:
    @staticmethod
    def serialize(object):
        return json.dumps(object)

    @staticmethod
    def deserialize(object):
        return json.loads(object)


class AddArticlePageService:
    def __check_form_data(self, request) -> bool:
        form_data = {
            "title": request.POST["title"],
            "content": request.POST["content"],
            "who_uploaded": "albina",
            "slug": randint(1, 10000000),
        }
        form = AddArticleForm(form_data, request.FILES)
        self.form = form
        return True if form.is_valid() else False

    def __save_form(self) -> QuerySet:
        return self.form.save()

    def __get_validation_errors(self) -> str:
        errors = ""
        logger.info(self.form.errors)
        for field in self.form.errors:
            for error in self.form.errors[field]:
                errors += error + ";"
        return errors

    @staticmethod
    def __allocate_space_for_marks(article_instance: QuerySet) -> None:
        ArticleMarkRepository.allocate_space_for_marks(article_instance)

    @staticmethod
    def __allocate_space_for_comments(article_instance: QuerySet) -> None:
        CommentRepository.allocate_space_for_comments(article_instance)

    @staticmethod
    def parse_validation_errors(errors) -> list:
        return errors.split(";")

    def execute_service(self, request) -> None or str:
        if self.__check_form_data(request):
            logger.info(self.__save_form())
            self.__allocate_space_for_marks(self.__save_form())
            self.__allocate_space_for_comments(self.__save_form())
        else:
            return self.__get_validation_errors()


class UserMarkService(Serializing):
    def __init__(
            self,
            article_id: int,
            user_email: str,
            mark: str,
    ):
        self.__article_id = article_id
        self.__user_email = user_email
        self.__new_mark = mark
        self.__mode = ""

    @staticmethod
    def get_likes_dislikes_count() -> list:
        likes = {}
        dislikes = {}
        marks = Mark.objects.all()
        for mark in marks:
            likes[mark.article_id] = len(UserMarkService.deserialize(mark.users_liked)["liked"])
            dislikes[mark.article_id] = len(UserMarkService.deserialize(mark.users_disliked)["disliked"])
        return [likes, dislikes]

    def __add_delete_like(self) -> None:
        article_likes_list, articles_likes_list = ArticleMarkRepository.get_mark_by_id(self.__article_id)
        new_users_who_liked = {"liked": UserMarkService.deserialize(article_likes_list.users_liked)["liked"]}
        if self.__mode == "add":
            new_users_who_liked["liked"].append(self.__user_email)
        elif self.__mode == "delete":
            new_users_who_liked["liked"].remove(self.__user_email)
        articles_likes_list.update(users_liked=UserMarkService.serialize(new_users_who_liked))

    def __add_delete_dislike(self) -> None:
        article_dislikes_list, articles_dislikes_list = ArticleMarkRepository.get_mark_by_id(self.__article_id)
        new_users_who_disliked = {"disliked": UserMarkService.deserialize(article_dislikes_list.users_disliked)["disliked"]}
        if self.__mode == "add":
            new_users_who_disliked["disliked"].append(self.__user_email)
        elif self.__mode == "delete":
            new_users_who_disliked["disliked"].remove(self.__user_email)
        articles_dislikes_list.update(users_disliked=UserMarkService.serialize(new_users_who_disliked))

    def __get_user_mark_status(self) -> str or None:
        marks, garbage = ArticleMarkRepository.get_mark_by_id(self.__article_id)
        users_who_liked = UserMarkService.deserialize(marks.users_liked)["liked"]
        users_who_disliked = UserMarkService.deserialize(marks.users_disliked)["disliked"]
        if self.__user_email in users_who_liked:
            return "liked"
        elif self.__user_email in users_who_disliked:
            return "disliked"

    def __set_mode_and_change_mark_status(self, current_mark: str) -> None:
        logger.info(self.__new_mark)
        if current_mark == "liked":
            logger.info("new mark: like")
            if self.__new_mark == "like":
                logger.info("new mark: like")
                self.__mode = "delete"
                self.__add_delete_like()
            else:
                logger.info("new mark: dislike")
                self.__mode = "delete"
                self.__add_delete_like()
                self.__mode = "add"
                self.__add_delete_dislike()
        elif current_mark == "disliked":
            logger.info("current mark: disliked")
            if self.__new_mark == "dislike":
                logger.info("new mark: dislike")
                self.__mode = "delete"
                self.__add_delete_dislike()
            else:
                logger.info("new mark: like")
                self.__mode = "delete"
                self.__add_delete_dislike()
                self.__mode = "add"
                self.__add_delete_like()
        else:
            self.__mode = "add"
            if self.__new_mark == "like":
                logger.info("new mark: like")
                self.__add_delete_like()
            else:
                logger.info("new mark: dislike")
                self.__add_delete_dislike()

    def execute(self) -> None:
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
        return True if "блять" not in self.__comment else False

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
