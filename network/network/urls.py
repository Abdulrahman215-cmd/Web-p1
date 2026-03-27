from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>/", views.profile_page, name="profile"),
    path("follow/", views.follow, name="follow"),
    path("toggle_follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
    path("update_post/<int:post_id>/", views.update_post, name="update_post"),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
]
