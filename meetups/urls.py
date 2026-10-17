from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", auth_views.LoginView.as_view(template_name="meetups/login.html", authentication_form=LoginForm), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("<slug:meetup_slug>/success", views.confirm_registration, name="confirm-registration"),
    path("<slug:meetup_slug>/edit", views.edit_meetup, name="edit-meetup"),
    path("<slug:meetup_slug>", views.meetup_details, name="meetup-detail"),
]
