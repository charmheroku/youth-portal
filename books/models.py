from django.utils import timezone
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


class ReadingSprint(models.Model):
    """
    Splits the reading into time-limited sprints (chapters/pages).
    """

    group = models.ForeignKey(
        ReadingGroup, on_delete=models.CASCADE, related_name="sprints"
    )
    name = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    chapters = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: 'Chapters 1–3' or 'Pages 10–25' or 'Block A'",
    )
    description = models.TextField(
        blank=True, help_text="Detailed explanation of what this sprint covers and why."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.group.book.title}"


class SprintProgress(models.Model):
    """
    Tracks if a user has completed reading a particular sprint.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sprint_progresses",
    )
    sprint = models.ForeignKey(
        ReadingSprint, on_delete=models.CASCADE, related_name="progress_entries"
    )
    is_read = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "sprint")

    def __str__(self):
        return (
            f"{self.user.email} - {self.sprint.name} "
            f"({'Read' if self.is_read else 'Not Read'})"
        )


class SprintIdea(models.Model):
    """
    Represents a key idea extracted by a participant from a reading sprint.
    """

    sprint = models.ForeignKey(
        ReadingSprint, on_delete=models.CASCADE, related_name="ideas"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sprint_ideas"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sprint", "user")

    def __str__(self):
        return f"Idea by {self.user.email} - {self.title} ({self.sprint.name})"


class IdeaDiscussion(models.Model):
    """
    Discussion under a specific sprint idea.
    """

    idea = models.ForeignKey(
        SprintIdea, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="idea_comments"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on '{self.idea.title}'"
