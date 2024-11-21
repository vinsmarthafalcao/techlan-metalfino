from django.urls import path
from . import views


urlpatterns = [
    path("autenticacao/login", views.login_view, name="login"),
    path("autenticacao/logout", views.logout_view, name="logout"),
    path("", views.home_view, name="home"),
]