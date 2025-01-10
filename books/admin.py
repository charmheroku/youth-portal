from django.contrib import admin
from books.models import Book, Vote


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin panel for managing books.
    """

    list_display = ("title", "author", "status", "total_votes")
    list_filter = ("status",)
    search_fields = ("title", "author")
    readonly_fields = ("total_votes",)

    def total_votes(self, obj):
        """
        Displays the total number of votes for a book.
        """
        return obj.votes.count()


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """
    Admin panel for managing votes.
    """

    list_display = ("user", "book", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "book__title")
