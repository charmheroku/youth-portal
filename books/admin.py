from django.contrib import admin
from books.models import Book, ReadingGroup, ReadingSprint, SprintProgress, Vote


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


@admin.register(ReadingGroup)
class ReadingGroupAdmin(admin.ModelAdmin):
    """
    Admin panel for managing reading groups.
    """

    list_display = ("book", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("book__title",)


@admin.register(ReadingSprint)
class ReadingSprintAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "description", "start_date", "end_date")
    list_filter = ("group", "start_date", "end_date")
    search_fields = ("name", "group__book__title")


@admin.register(SprintProgress)
class SprintProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "sprint", "is_read", "completed_at", "updated_at")
    list_filter = ("is_read", "sprint__group")
    search_fields = ("user__email", "sprint__name")
