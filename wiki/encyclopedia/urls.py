from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry_page, name="entry_page"),
    path("search/", views.search, name="search"),
    path("create/", views.create_page, name="create"),
    path("<str:title>/edit/", views.edit_page, name="edit"),
    path("random/", views.random_page, name="random")
]
