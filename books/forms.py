from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for creating or updating a Book.
    """

    class Meta:
        model = Book
        fields = ["title", "author", "description", "cover", "status"]
