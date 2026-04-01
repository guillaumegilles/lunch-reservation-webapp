from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("save-lunch/", views.save_lunch, name="save_lunch"),
    path("admin-summary/", views.admin_summary, name="admin_summary"),
]
