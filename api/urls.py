from django.urls import path
from .views import MarkView, CommentView


urlpatterns = [
    path("mark/", MarkView.as_view()),
    path("comment/", CommentView.as_view()),
]
