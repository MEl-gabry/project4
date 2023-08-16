
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),
    path("posts/<int:pg>", views.posts, name="posts"),
    path("user", views.user, name="user"),
    path("following", views.following, name="following"),
    path("fposts/<int:pg>", views.following_posts, name="fposts"),
    path("follow/<str:user>", views.follow, name="follow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
