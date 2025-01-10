from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Book
from .forms import BookForm


class BookListView(ListView):
    """
    Displays the list of all books.
    """

    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"


class BookDetailView(DetailView):
    """
    Shows details of a specific book, including cover and description.
    """

    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"


class BookCreateView(CreateView):
    """
    Allows admin (or staff) to create a new book.
    """

    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_list")


class BookUpdateView(UpdateView):
    """
    Allows admin (or staff) to edit an existing book.
    """

    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_list")


class BookDeleteView(DeleteView):
    """
    Allows admin (or staff) to delete a book.
    """

    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("books:book_list")
