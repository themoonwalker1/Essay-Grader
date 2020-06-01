from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("create", views.create, name="create"),
    path("setup", views.setup, name="setup"),
    path("home", views.index, name="home"),
    path("<int:pk>/", views.detail, name="detail"),
    path("submit", views.submit, name="submit"),
    path("teacher/home", views.teacher, name="teacher"),
    path("teacher/<int:pk>/", views.teacher_detail, name="teacher_detail"),
    path("teacher/<int:pk>/grade", views.grade, name="grade"),
    path("settings/", views.settings, name="settings"),
]
