import logging
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import views
from core.repository import ArticleMarkRepository, CommentRepository
from core.models import Article
from rest_framework.request import Request
from core.services import UserMarkService, UserCommentService


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
        return Response({"success": True})


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
            return Response({"success": False})

        return Response({"success": True})
