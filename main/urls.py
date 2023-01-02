from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name="home"),
    path("article/<int:pk>", views.article_details, name="article_details"),
    path("tag/<int:pk>", views.tag_list, name="tag_list"),
    path("publish", views.create_article, name="create_article"),
    path("delete_article/<int:pk>", views.delete_article, name="delete_article"),
    path("edit_article/<int:pk>", views.edit_article, name="edit_article"),
    path("article_archive/<int:year>/<int:month>", views.article_archive, name="article_archive"),
    path("profile/<int:pk>", views.get_profile, name="profile"),
    path("edit_profile/<int:pk>", views.edit_profile, name="edit_profile"),
]

htmx_urlpatterns = [
    path("like_article/<int:pk>", views.like_article, name = "like_article"),
]

urlpatterns += htmx_urlpatterns