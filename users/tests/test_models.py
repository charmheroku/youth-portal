from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from users.models import CustomUser

User = get_user_model()


class CustomUserModelTest(TestCase):
    """
    Tests for the CustomUser model:
    - Creation and saving
    - Unique email constraint
    - __str__ method
    """

    def setUp(self) -> None:
        """
        Create an existing user in the database for use in tests.
        """
        self.user = CustomUser.objects.create_user(
            username="test_user",
            email="existing@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )

    def test_create_custom_user(self) -> None:
        """
        Verifies a user is properly created and saved,
        checking fields like email, first/last name, etc.
        """
        user_count_before = CustomUser.objects.count()

        new_user = CustomUser.objects.create_user(
            username="test_user_new",
            email="new@example.com",
            password="newpass",
            first_name="Jane",
            last_name="Smith",
        )
        user_count_after = CustomUser.objects.count()

        self.assertEqual(user_count_after, user_count_before + 1)
        self.assertTrue(check_password("newpass", new_user.password))
        self.assertEqual(new_user.username, "test_user_new")
        self.assertEqual(new_user.email, "new@example.com")
        self.assertEqual(new_user.first_name, "Jane")
        self.assertEqual(new_user.last_name, "Smith")

    def test_unique_email_constraint(self) -> None:
        """
        Ensures creating a user with an existing email
        raises an error (e.g., IntegrityError).
        """
        with self.assertRaises(Exception):  # Could be IntegrityError
            CustomUser.objects.create_user(
                email="existing@example.com", password="anotherpass"
            )

    def test_user_str_representation(self) -> None:
        """
        By default, __str__() returns the user's email in CustomUser.
        """
        self.assertEqual(str(self.user), "existing@example.com")
