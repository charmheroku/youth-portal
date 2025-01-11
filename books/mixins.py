from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Custom mixin to restrict access to admin users only.
    """

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.warning(
            self.request, "You do not have permission to access this page."
        )
        return redirect("books:book_list")
