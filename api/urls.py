from django.urls import path
from .views import MarkView, CommentView, UserView


urlpatterns = [
    path("mark", MarkView.as_view(), name="mark_"),
    path("comment", CommentView.as_view(), name="comment_"),
    path("user", UserView.as_view(), name="user_"),
]
