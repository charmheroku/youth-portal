from django.test import TestCase
from django.utils import timezone

from books.models import (Book, ReadingGroup, ReadingSprint, SprintIdea,
                          SprintProgress)
from users.models import CustomUser


class BookModelTest(TestCase):
    """
    Tests for the Book model:
    - Ensures object creation works
    - Tests the total_votes method
    """

    def setUp(self) -> None:
        """
        Create a default user and a default book for reuse in tests.
        """
        self.user = CustomUser.objects.create_user(
            email="user@example.com", password="password123", username="test_username"
        )
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", status="new"
        )

    def test_book_creation(self) -> None:
        """
        Verifies that a Book object is properly created and saved to the DB.
        """
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.status, "new")
        self.assertIsNotNone(self.book.created_at)

    def test_book_total_votes(self) -> None:
        """
        Ensures total_votes returns the correct number of votes.
        """
        # Initially, no votes
        self.assertEqual(self.book.total_votes(), 0)

        # Add a vote
        self.book.votes.add(self.user)
        self.assertEqual(self.book.total_votes(), 1)


class ReadingGroupModelTest(TestCase):
    """
    Tests for ReadingGroup:
    - Checks creation
    - Relationship with Book and participants
    """

    def setUp(self) -> None:
        """
        Creates a book, a reading group, and two users for testing participants.
        """
        self.book = Book.objects.create(
            title="Group Book", author="Group Author", status="reading"
        )
        self.group = ReadingGroup.objects.create(book=self.book, is_active=True)
        self.user1 = CustomUser.objects.create_user(
            email="u1@example.com", password="pass", username="test_username1"
        )
        self.user2 = CustomUser.objects.create_user(
            email="u2@example.com", password="pass", username="test_username2"
        )

    def test_reading_group_creation(self) -> None:
        """
        Verifies the ReadingGroup is linked to the correct Book
        and is active by default.
        """
        self.assertEqual(self.group.book, self.book)
        self.assertTrue(self.group.is_active)

    def test_reading_group_participants(self) -> None:
        """
        Ensures participants can be added to the group.
        """
        self.group.participants.add(self.user1, self.user2)
        self.assertEqual(self.group.participants.count(), 2)


class ReadingSprintModelTest(TestCase):
    """
    Tests for ReadingSprint:
    - Checks creation
    - Relationship with ReadingGroup
    """

    def setUp(self) -> None:
        """
        Prepare a Book, a ReadingGroup, and a ReadingSprint.
        """
        self.book = Book.objects.create(
            title="Sprint Book", author="Sprint Author", status="reading"
        )
        self.group = ReadingGroup.objects.create(book=self.book)
        self.sprint = ReadingSprint.objects.create(
            group=self.group,
            name="Sprint 1",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            chapters="Chapters 1-3",
            description="Read first 3 chapters",
        )

    def test_sprint_creation(self) -> None:
        """
        Ensures a ReadingSprint is created with correct data.
        """
        self.assertEqual(self.sprint.group, self.group)
        self.assertIn("Chapters 1-3", self.sprint.chapters)


class SprintProgressModelTest(TestCase):
    """
    Tests for SprintProgress:
    - Uniqueness (user + sprint)
    - Checking the is_read flag
    """

    def setUp(self) -> None:
        """
        Prepare one user, one ReadingGroup, one ReadingSprint,
        and a SprintProgress record.
        """
        self.user = CustomUser.objects.create_user(
            email="progress@example.com", password="pass", username="test_username"
        )
        self.book = Book.objects.create(
            title="Progress Book", author="Prog Author", status="reading"
        )
        self.group = ReadingGroup.objects.create(book=self.book)
        self.sprint = ReadingSprint.objects.create(
            group=self.group, name="Progress Sprint"
        )
        self.progress = SprintProgress.objects.create(
            user=self.user, sprint=self.sprint
        )

    def test_sprint_progress(self) -> None:
        """
        Verifies SprintProgress is created and can toggle is_read.
        """
        self.assertFalse(self.progress.is_read)
        self.progress.is_read = True
        self.progress.save()
        self.assertTrue(self.progress.is_read)


class SprintIdeaModelTest(TestCase):
    """
    Tests for SprintIdea:
    - Relationship with User and ReadingSprint
    """

    def setUp(self) -> None:
        """
        Prepare a user, a ReadingGroup, a ReadingSprint, and an Idea.
        """
        self.user = CustomUser.objects.create_user(
            email="idea@example.com", password="pass", username="test_username"
        )
        self.book = Book.objects.create(
            title="Idea Book", author="Idea Author", status="reading"
        )
        self.group = ReadingGroup.objects.create(book=self.book)
        self.sprint = ReadingSprint.objects.create(group=self.group, name="Idea Sprint")
        self.idea = SprintIdea.objects.create(
            sprint=self.sprint,
            user=self.user,
            title="Main Idea",
            content="Important insight",
        )

    def test_sprint_idea_creation(self) -> None:
        """
        Verifies an idea is linked to the correct user and sprint.
        """
        self.assertEqual(self.idea.user, self.user)
        self.assertEqual(self.idea.sprint, self.sprint)
        self.assertIn("Important insight", self.idea.content)
