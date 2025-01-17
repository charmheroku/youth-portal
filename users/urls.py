from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import ProfileView, UserSignUpView

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

app_name = "users"
