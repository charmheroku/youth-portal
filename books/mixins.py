from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Custom mixin to allow access only for staff users.
    """

    def test_func(self):
        return self.request.user.is_staff
