from django.test import TestCase
from django.utils import timezone

from books.models import Book, ReadingGroup, ReadingSprint, SprintProgress
from users.models import CustomUser


class SprintSignalTest(TestCase):
    """
    Tests for the create_sprint_progress signal:
    - Check automatic creation of SprintProgress when a new ReadingSprint is created
    """

    def setUp(self) -> None:
        self.user1 = CustomUser.objects.create_user(
            email="user1@example.com", password="pass1", username="test_username"
        )
        self.user2 = CustomUser.objects.create_user(
            email="user2@example.com", password="pass2", username="test_username2"
        )
        self.book = Book.objects.create(
            title="Signal Book", author="Signal Author", status="reading"
        )
        self.group = ReadingGroup.objects.create(book=self.book, is_active=True)
        self.group.participants.set([self.user1, self.user2])

    def test_create_sprint_progress_signal(self) -> None:
        """
        Ensures that creating a new ReadingSprint automatically creates
        SprintProgress entries for all group participants.
        """
        sprint = ReadingSprint.objects.create(
            group=self.group,
            name="Signal Sprint",
            start_date=timezone.now(),
            end_date=timezone.now(),
        )
        # Check that a SprintProgress record was created for each participant
        progress_records = SprintProgress.objects.filter(sprint=sprint)
        self.assertEqual(progress_records.count(), 2)
        user_emails = progress_records.values_list("user__email", flat=True)
        self.assertIn("user1@example.com", user_emails)
        self.assertIn("user2@example.com", user_emails)
