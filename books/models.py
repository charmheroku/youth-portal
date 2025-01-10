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

    def __str__(self) -> str:
        return f"{self.title} by {self.author} ({self.status})"
