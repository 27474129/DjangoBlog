from django.urls import path, reverse
from .views import IndexPage, AddArticlePage, ArticlePage, article_url_plut


urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("addarticle/", AddArticlePage.as_view(), name="addarticle"),
    path("article/", article_url_plut, name="article"),
    path("article/<slug:article_slug>", ArticlePage.as_view(), name="specific_article"),
]
