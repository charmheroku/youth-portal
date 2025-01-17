from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from users.forms import SignUpForm
from users.models import CustomUser


class UserSignUpView(CreateView):
    """User registration view using Django's CreateView"""

    model = CustomUser
    form_class = SignUpForm
    template_name = "users/signup.html"

    def form_valid(self, form):
        """Log in user after successful signup"""
        self.object = form.save()
        login(self.request, self.object)
        return redirect(reverse_lazy("users:profile"))


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Profile page for authenticated users.
    """

    model = CustomUser
    template_name = "users/profile.html"
    context_object_name = "user_profile"

    def get_object(self):
        """
        Returns the currently logged-in user as the object.
        """
        return self.request.user
