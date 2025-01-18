from django.test import TestCase
from books.forms import BookForm, SprintIdeaForm
from books.models import Book


class BookFormTest(TestCase):
    """
    Tests for the BookForm:
    - Validate correct data
    - Saving data
    """

    def setUp(self) -> None:
        """
        Prepare form data for testing.
        """
        self.valid_data = {
            "title": "Form Test Book",
            "author": "Form Test Author",
            "description": "Some description",
            "status": "new",
        }

    def test_book_form_valid_data(self) -> None:
        """
        Ensures the form is valid with correct data.
        """
        form = BookForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), "Form should be valid with correct data.")

    def test_book_form_save(self) -> None:
        """
        Checks that the form saves data to the DB correctly.
        """
        form = BookForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        book = form.save()
        self.assertIsInstance(book, Book)
        self.assertEqual(book.title, "Form Test Book")


class SprintIdeaFormTest(TestCase):
    """
    Tests for SprintIdeaForm:
    - Checks required fields
    - Validation
    """

    def setUp(self) -> None:
        """
        Prepare valid and invalid data for the form.
        """
        self.valid_data = {
            "title": "Insightful Title",
            "content": "Interesting content about the sprint.",
        }
        self.invalid_data = {"title": "", "content": "Content without a title."}

    def test_sprint_idea_form_valid_data(self) -> None:
        """
        Ensures the form is valid with correct data.
        """
        form = SprintIdeaForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_sprint_idea_form_missing_title(self) -> None:
        """
        Ensures the form is invalid if 'title' is empty.
        """
        form = SprintIdeaForm(data=self.invalid_data)
        self.assertFalse(form.is_valid(), "Form should be invalid when title is empty.")
