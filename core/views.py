import logging
from django.views import View
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.base import TemplateView
from .models import Article
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .forms import AddArticleForm
from django.shortcuts import render
from .services import AddArticlePageService
from django.db.models import F
from api.services import UserMarkService
from django.http import HttpResponseNotFound
from .repository import ArticleRepository


logger = logging.getLogger("debug")


class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(e)
            return HttpResponseRedirect(reverse("index"))


class IndexPage(BaseView, ListView):
    template_name = "core/index.html"
    model = Article
    context_object_name = "articles"
    user_email = None

    def get(self, request, *args, **kwargs):
        if "email" in request.session:
            self.user_email = request.session.get("email")
            logger.info(f"Logged in yet with: {request.session.get('email')}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        marks = UserMarkService.get_likes_dislikes_count()
        context["likes"] = marks[0]
        context["dislikes"] = marks[1]
        context["user_email"] = self.user_email
        return context


class AddArticlePage(BaseView, TemplateView):
    template_name = "core/addarticle.html"
    errors = str()

    def get(self, request, *args, **kwargs):
        self.errors = AddArticlePageService.parse_validation_errors(request.GET["errors"]) if "errors" in request.GET else []
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        errors = AddArticlePageService().execute_service(request)
        if errors is None:
            return HttpResponseRedirect(reverse_lazy("index"))
        return HttpResponseRedirect(reverse_lazy("addarticle") + "?errors=" + errors)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddArticleForm()
        context["errors"] = self.errors
        return context


class ArticlePage(TemplateView):
    template_name = "core/article.html"
    article = None

    def get(self, request, *args, **kwargs):
        article = ArticleRepository.get_article_by_slug(kwargs["article_slug"])
        if article is None or not article.is_published:
            return HttpResponseNotFound()
        self.article = article
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = self.article
        return context


def article_url_plut(request) -> HttpResponseNotFound:
    return HttpResponseNotFound()
