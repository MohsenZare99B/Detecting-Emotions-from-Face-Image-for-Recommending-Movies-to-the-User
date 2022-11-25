from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("movie/<str:pk>/", views.movie, name='movie'),
    path("movies/", views.movies, name='movies'),
    path("login_user/", views.login_user, name='login_user'),
    path("logout_user/", views.logout_user, name='logout_user'),
    path("register_user/", views.register_user, name='register_user'),
    path("user_upload/", views.user_upload, name="user_upload"),
    path("result/", views.result, name="result"),
    path("comment/<str:pk>", views.comment, name="comment"),
]