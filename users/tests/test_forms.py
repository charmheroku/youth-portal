from django.test import TestCase

from users.forms import SignUpForm
from users.models import CustomUser


class SignUpFormTest(TestCase):
    """
    Tests for the SignUpForm:
    - Valid data scenario
    - Duplicate email check
    - Password mismatch
    """

    def setUp(self) -> None:
        """
        Create an existing user to test duplicate email scenario.
        """
        CustomUser.objects.create_user(
            email="existing@example.com", password="password123", username="test_user"
        )

    def test_signup_form_valid_data(self) -> None:
        """
        Checks that the form is valid with proper data and saves user correctly.
        """
        form_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "newuser@example.com",
            "gender": "male",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(
            form.is_valid(),
            "Form should be valid with matching passwords and unique email.",
        )
        user = form.save()
        self.assertEqual(user.email, "newuser@example.com")

    def test_signup_form_duplicate_email(self) -> None:
        """
        Form should be invalid if the email already exists in the database.
        """
        form_data = {
            "first_name": "Test2",
            "last_name": "User2",
            "email": "existing@example.com",  # already taken
            "gender": "female",
            "password1": "AnotherPass123",
            "password2": "AnotherPass123",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_password_mismatch(self) -> None:
        """
        Form should be invalid if password1 != password2.
        """
        form_data = {
            "first_name": "Mismatch",
            "last_name": "Test",
            "email": "mismatch@example.com",
            "gender": "male",
            "password1": "Pass1234",
            "password2": "Pass4567",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
