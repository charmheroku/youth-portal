from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class UserViewsTest(TestCase):
    """
    Tests for user-related views:
    - SignUp (UserSignUpView)
    - Profile (ProfileView)
    - Login & Logout
    """

    def setUp(self) -> None:
        """
        Create a normal user and define URL paths for reuse.
        """
        self.user = CustomUser.objects.create_user(
            username="test_user",
            email="normal@example.com",
            password="normalpass",
            first_name="Normal",
            last_name="User",
        )
        self.signup_url = reverse("users:signup")
        self.profile_url = reverse("users:profile")
        self.login_url = reverse("users:login")
        self.logout_url = reverse("users:logout")

    def test_signup_view_get(self) -> None:
        """
        Ensures GET to the signup view returns a 200 and uses the correct template.
        """
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/signup.html")

    def test_signup_view_post_valid(self) -> None:
        """
        If valid data is posted, a new user should be created and logged
        in automatically.
        """
        response = self.client.post(
            self.signup_url,
            {
                "first_name": "Test",
                "last_name": "SignUp",
                "email": "signup@example.com",
                "gender": "male",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            },
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(CustomUser.objects.filter(email="signup@example.com").exists())

        self.assertIn(SESSION_KEY, self.client.session)

    def test_profile_view_unauthenticated(self) -> None:
        """
        Unauthenticated users should be redirected to login when accessing profile.
        """
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.url, self.profile_url)

    def test_profile_view_authenticated(self) -> None:
        """
        Authenticated users should see the profile page (200 OK).
        """
        self.client.login(email="normal@example.com", password="normalpass")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_login_view(self) -> None:
        """
        Checks that an existing user can log in with correct credentials.
        """
        response = self.client.post(
            self.login_url,
            {
                "username": "normal@example.com",
                "password": "normalpass",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_logout_view(self) -> None:
        """
        Logs out a user and confirms the session is cleared.
        """
        self.client.login(email="normal@example.com", password="normalpass")
        self.assertIn(SESSION_KEY, self.client.session)

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(
            SESSION_KEY, self.client.session, "Session should be cleared after logout."
        )
