from django.test import TestCase
from django.urls import reverse

from books.models import Book, Vote, ReadingGroup
from users.models import CustomUser


class ToggleVoteViewTest(TestCase):
    """
    Tests for ToggleVoteView:
    - Vote addition and removal
    - Login requirement
    """

    def setUp(self) -> None:
        """
        Prepare a user and a book for testing the toggle voting view.
        """
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="password123", username="test_username"
        )
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", status="new"
        )
        self.toggle_vote_url = reverse("books:toggle_vote", kwargs={"pk": self.book.pk})

    def test_toggle_vote_add_and_remove(self) -> None:
        """
        Ensures a user can add a vote to a book and then remove it.
        """
        self.client.login(
            email=self.user.email, password="password123")

        self.assertFalse(Vote.objects.filter(user=self.user, book=self.book).exists())

        self.client.post(self.toggle_vote_url)
        self.assertTrue(Vote.objects.filter(user=self.user, book=self.book).exists())

        self.client.post(self.toggle_vote_url)
        self.assertFalse(Vote.objects.filter(user=self.user, book=self.book).exists())

    def test_toggle_vote_unauthenticated(self) -> None:
        """
        Ensures an unauthenticated user can't vote.
        """
        response = self.client.post(self.toggle_vote_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Vote.objects.filter(book=self.book).exists())


class CreateReadingGroupViewTest(TestCase):
    """
    Tests for the CreateReadingGroup view (finalize_voting):
    - Checks creation of a reading group
    - Changes book status to 'reading'
    - Admin-only access
    """

    def setUp(self) -> None:
        """
        Prepare admin user, normal user, and a book with status 'voting'.
        """
        self.admin_user = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpass",
            username="test_username_admin"
        )
        self.normal_user = CustomUser.objects.create_user(
            email="user@example.com", password="userpass", username="test_username"
        )
        self.book = Book.objects.create(
            title="Voting Book", author="Author", status="voting"
        )
        self.finalize_url = reverse(
            "books:finalize_voting", kwargs={"pk": self.book.pk}
        )

    def test_create_reading_group_as_admin(self) -> None:
        """
        Admin can finalize voting, create a group,
        and the book status changes to 'reading'.
        """
        self.client.login(email="admin@example.com", password="adminpass")
        response = self.client.post(self.finalize_url)
        self.assertRedirects(response, reverse("books:group_detail", kwargs={"pk": 1}))

        self.book.refresh_from_db()
        self.assertEqual(self.book.status, "reading")
        self.assertTrue(ReadingGroup.objects.filter(book=self.book).exists())

    def test_create_reading_group_as_normal_user(self) -> None:
        """
        Normal users should not be able to finalize voting.
        """
        self.client.login(email="user@example.com", password="userpass")
        response = self.client.post(self.finalize_url)

        self.assertRedirects(response, reverse("books:book_list"))
        self.assertFalse(ReadingGroup.objects.filter(book=self.book).exists())
