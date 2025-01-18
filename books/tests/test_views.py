from django.test import TestCase
from django.urls import reverse

from books.models import (
    Book,
    HeroSection,
    ReadingGroup,
    ReadingSprint,
    SprintIdea,
    Vote,
)
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
        self.client.login(email=self.user.email, password="password123")

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
            email="admin@example.com",
            password="adminpass",
            username="test_username_admin",
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


class GlobalSearchTest(TestCase):
    """
    Tests for global search functionality.
    """

    def setUp(self):
        """
        Set up test data for global search tests.
        """
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="password123", username="testuser"
        )
        self.book = Book.objects.create(
            title="Test Book", author="Author", status="new"
        )
        self.group = ReadingGroup.objects.create(book=self.book, is_active=True)
        self.sprint = ReadingSprint.objects.create(
            group=self.group, name="Sprint 1", start_date="2023-01-01"
        )
        self.idea = SprintIdea.objects.create(
            sprint=self.sprint, user=self.user, title="Test Idea", content="Content"
        )
        self.global_search_url = reverse("books:global_search")

    def test_search_books(self):
        """
        Test search functionality for books.
        """
        response = self.client.get(f"{self.global_search_url}?q=Test&category=books")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_search_groups(self):
        """
        Test search functionality for groups.
        """
        response = self.client.get(f"{self.global_search_url}?q=Test&category=groups")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.group.book.title)

    def test_search_ideas(self):
        """
        Test search functionality for ideas.
        """
        response = self.client.get(f"{self.global_search_url}?q=Test&category=ideas")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.idea.title)

    def test_empty_query(self):
        """
        Test that all items are returned when query is empty.
        """
        response = self.client.get(self.global_search_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.group.book.title)
        self.assertContains(response, self.idea.title)


class BooksHomeTest(TestCase):
    """
    Tests for the books_home view.
    """

    def setUp(self):
        """
        Set up test data for books_home.
        """
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="password123", username="testuser"
        )

        self.new_book = Book.objects.create(
            title="New Book", author="Author", status="new"
        )
        self.voting_book = Book.objects.create(
            title="Voting Book", author="Author", status="voting"
        )
        self.finished_book = Book.objects.create(
            title="Finished Book", author="Author", status="finished"
        )
        self.reading_book = Book.objects.create(
            title="Reading Book", author="Author", status="reading"
        )

        self.group = ReadingGroup.objects.create(
            book=self.reading_book,
            is_active=True,
        )

        self.sprint = ReadingSprint.objects.create(
            group=self.group,
            name="Sprint 1",
            chapters="Chapters 1-5",
        )

        self.idea = SprintIdea.objects.create(
            sprint=self.sprint,
            user=self.user,
            title="Idea Title",
            content="Idea Content",
        )

        self.hero_section = HeroSection.objects.create(
            title="Welcome!", subtitle="Discover new books.", background=None
        )

        self.books_home_url = reverse("books:books_home")

    def test_books_home_template(self):
        """
        Test that the correct template is used for books_home.
        """
        response = self.client.get(self.books_home_url)
        self.assertTemplateUsed(response, "books/books_home.html")

    def test_books_home_context(self):
        """
        Test that the context data is correctly passed to the template.
        """
        response = self.client.get(self.books_home_url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["total_users"], 1)
        self.assertEqual(response.context["total_groups_reading"], 1)
        self.assertEqual(response.context["total_ideas"], 1)
        self.assertEqual(response.context["total_completed_books"], 1)
        self.assertEqual(response.context["current_book"], self.reading_book)
        self.assertIn(self.new_book, response.context["latest_books"])
        self.assertIn(self.voting_book, response.context["voting_books"])
        self.assertIn(self.finished_book, response.context["completed_books"])
        self.assertEqual(response.context["hero_background"], self.hero_section)
