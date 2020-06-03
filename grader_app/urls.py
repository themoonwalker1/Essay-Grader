from django.urls import path, re_path
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
    path('ajax/load-assignments/', views.load_assignments, name='ajax_load_assignments'),
    path("teacher/home", views.teacher, name="teacher"),
    path("teacher/assignment", views.assignment, name="assignment"),
    path("teacher/<int:pk>/", views.teacher_detail, name="teacher_detail"),
    path("teacher/<int:pk1>/<int:pk2>/", views.teacher_essays, name="teacher_detail_essay"),
    path("teacher/<int:pk>/grade", views.grade, name="grade"),
    path("settings/info", views.settings_changeInfo, name="settings_info"),
    path("settings/password", views.settings_changePassword, name="settings_password"),
    path("settings/teachers", views.settings_changeTeachers, name="settings_teachers"),
]
