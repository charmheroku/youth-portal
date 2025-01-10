from django.conf import settings
from django.db import models


class Book(models.Model):
    """
    Represents a book in the library, with a cover image and description.
    """

    STATUS_CHOICES = [
        ("new", "New"),
        ("voting", "Voting"),
        ("reading", "Reading"),
        ("finished", "Finished"),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Vote", related_name="voted_books"
    )

    def total_votes(self):
        """
        Returns the total number of votes for this book.
        """
        return self.votes.count()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.status})"


class Vote(models.Model):
    """
    Model representing a user's vote for a book.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")


class ReadingGroup(models.Model):
    """
    Group for users reading a book together.
    """

    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, related_name="reading_group"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="reading_groups", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Reading Group for {self.book.title}"
