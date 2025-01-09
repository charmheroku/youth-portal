from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView
from users.models import CustomUser
from users.forms import SignUpForm


class UserSignUpView(CreateView):
    """User registration view using Django's CreateView"""

    model = CustomUser
    form_class = SignUpForm
    template_name = "users/signup.html"
    success_url = "/"

    def form_valid(self, form):
        """Log in user after successful signup"""
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)
