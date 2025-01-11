from django import forms
from .models import Book, ReadingSprint


class BookForm(forms.ModelForm):
    """
    Form for creating or updating a Book.
    """

    class Meta:
        model = Book
        fields = ["title", "author", "description", "cover", "status"]


class ReadingSprintForm(forms.ModelForm):
    class Meta:
        model = ReadingSprint
        fields = ["name", "start_date", "end_date", "chapters", "description"]
