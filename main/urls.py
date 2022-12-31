from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name = "home"),
    path("article/<int:pk>", views.article_details, name = "article_details"),
    # path("tag/<int:pk>", views.tag_details, name = "tag_details"),
    path("publish", views.create_article, name = "create_article"),
    # path("delete_article/<int:pk>", views.delete_article, name = "delete_article"),
    # path("edit_article/<int:pk>", views.edit_article, name = "edit_article"),
    path("profile/<int:pk>", views.get_profile, name = "profile"),
]

htmx_urlpatterns = [
    # path("like_article/<int:pk>", views.like_article, name = "like_article"),
]

urlpatterns += htmx_urlpatterns