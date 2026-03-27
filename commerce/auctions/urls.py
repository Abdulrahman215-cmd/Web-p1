from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create"),
    path("list_item/<str:title>/", views.list_item, name="list_item"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("toggle_watchlist/<str:title>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("Category/", views.category, name="category"),
    path("Category/<str:category_name>", views.filter, name="filter")
]
