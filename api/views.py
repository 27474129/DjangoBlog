import logging
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import views
from core.repository import ArticleRepository
from .repository import CommentRepository, MarkRepository
from core.models import Article
from rest_framework.request import Request
from .services import UserMarkService, UserCommentService
from core.repository import ArticleRepository
from users.repository import UserRepository
from .serializers import UserSerializer
from users.validators import UserValidators
from .services import Serializing
from rest_framework.renderers import JSONRenderer


logger = logging.getLogger("debug")


class BaseAPIView(views.APIView):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(e)
            return Response({"error": e})


class MarkView(BaseAPIView):
    def put(self, request):
        user_email = request.query_params["user_email"]
        article_id = int(request.query_params["article_id"])
        mark = request.query_params["mark"]

        UserMarkService(
            article_id=article_id,
            user_email=user_email,
            mark=mark
        ).execute()
        json_response = JSONRenderer().render([{"success": True}])
        return Response(json_response)


class CommentView(BaseAPIView):
    def post(self, request):
        article_id = request.query_params["article_id"]
        user_email = request.query_params["user_email"]
        comment = request.query_params['comment']
        comment_adding_result = UserCommentService(
            article_id=article_id,
            user_email=user_email,
            comment=comment,
        ).execute()
        if not comment_adding_result:
            return Response(JSONRenderer().render([{"success": True}]))

        return Response(JSONRenderer().render([{"success": True}]))


class UserView(BaseAPIView):
    def get(self, request):
        users = UserRepository.get_all()
        return Response(JSONRenderer().render([{"success": True, "users": UserSerializer(users, many=True).data}]))

    def post(self, request):
        serializer = UserSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        errors = UserValidators().execute_validators(data=request.query_params)
        if len(errors) == 0:
            serializer.save()
            return Response(JSONRenderer().render([{"success": True, "new_user": serializer.data}]))
        else:
            return Response(JSONRenderer().render([{"success": False, "errors": errors}]), status=400)

    def put(self, request):
        pk = request.query_params.get("pk", None)
        if pk is None:
            return Response(JSONRenderer().render([{"success": False, "error": "Вы не передали параметр id"}]), status=400)

        if len(request.query_params) != 2:
            return Response(JSONRenderer().render([{"success": False, "error": "Слишком много аргументов в запросе"}]), status=400)

        user = UserRepository.get_user_by_pk(pk)
        if user is None:
            return Response(JSONRenderer().render([{"success": False, "error": "Пользователь с таким id не найден"}]), status=404)

        data = {
            "firstname": request.query_params.get("firstname", None),
            "secondname": request.query_params.get("secondname", None),
            "email": request.query_params.get("email", None),
            "password": request.query_params.get("password", None),
        }
        if data["firstname"] is None:
            data["firstname"] = user.firstname
        if data["secondname"] is None:
            data["secondname"] = user.secondname
        if data["email"] is None:
            data["email"] = user.email
        if data["password"] is None:
            data["password"] = user.password

        serializer = UserSerializer(data=data, instance=user)
        serializer.is_valid(raise_exception=True)

        if request.query_params.get("email", None) is not None:
            errors = UserValidators().execute_validators(data=data)
        else:
            errors = UserValidators().execute_validators(data=data, mode="without_email_validation")

        if len(errors) == 0:
            serializer.save()
            return Response(JSONRenderer().render([{"success": True, "updated_user": serializer.data}]))
        else:
            return Response(JSONRenderer().render([{"success": False, "errors": errors}]), status=400)

    def delete(self, request):
        pk = request.query_params.get("pk", None)
        if pk is None:
            return Response(JSONRenderer().render([{"success": False, "error": "Вы не передали id записи"}]), status=400)

        deleted_user = UserRepository.delete_user(pk)

        if deleted_user is not None:
            return Response(JSONRenderer().render([{"success": True}]))
        else:
            return Response(JSONRenderer().render([{"success": False, "error": "Юзер не существует"}]), status=404)
