import logging
import requests
from django import template
from core.services import UserMarkService, UserCommentService
from django.urls import reverse, reverse_lazy


logger = logging.getLogger("debug")
register = template.Library()


def get_article_url(slug: int) -> str:
    return reverse("article") + str(slug)


register.filter("get_article_url", get_article_url)
