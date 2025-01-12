from django import forms
from .models import Book, IdeaDiscussion, ReadingSprint, SprintIdea


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


class SprintIdeaForm(forms.ModelForm):
    class Meta:
        model = SprintIdea
        fields = ["title", "content"]


class IdeaDiscussionForm(forms.ModelForm):
    class Meta:
        model = IdeaDiscussion
        fields = ["comment"]
