from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('search/', views.search, name='search'),
    path("profile/<str:username>/", views.profile_page, name="profile"),
    path('get_directions/', views.get_directions, name='get_directions'),
]
