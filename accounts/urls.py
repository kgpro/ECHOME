# accounts/urls.py
from django.urls import path
from . import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("signup/", auth_views.signup, name="signup"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    # add social/google endpoints if you need them (we already added custom Google earlier if desired)
]
