from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser


class SignUpForm(UserCreationForm):
    """User registration form"""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="",
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "gender",
            "password1",
            "password2",
        )

    def clean_email(self):
        """Validate email"""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        user.username = email
        user.save()
        return user
