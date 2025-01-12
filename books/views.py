from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Book, ReadingGroup, ReadingSprint, SprintIdea, SprintProgress, Vote
from .forms import BookForm, IdeaDiscussionForm, ReadingSprintForm, SprintIdeaForm
from .mixins import AdminRequiredMixin


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


class BookCreateView(AdminRequiredMixin, CreateView):
    """
    Allows admin (or staff) to create a new book.
    """

    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_list")


class BookUpdateView(AdminRequiredMixin, UpdateView):
    """
    Allows admin (or staff) to edit an existing book.
    """

    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_list")


class BookDeleteView(AdminRequiredMixin, DeleteView):
    """
    Allows admin (or staff) to delete a book.
    """

    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("books:book_list")


class ToggleVoteView(LoginRequiredMixin, View):
    """
    Toggle voting for a book. If the user has already voted, remove the vote.
    """

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=kwargs["pk"])
        vote, created = Vote.objects.get_or_create(user=request.user, book=book)

        if not created:
            vote.delete()
            messages.success(request, "Your vote has been removed.")
        else:
            messages.success(request, "You voted for this book!")

        return redirect("books:book_list")


class CreateReadingGroup(AdminRequiredMixin, View):
    """
    Admin finalizes voting, changes book status to 'reading' and creates a group.
    """

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs["pk"])

        if book.status == "reading":
            messages.warning(
                request, "This book is already being read. You cannot vote for it."
            )
            return redirect("books:book_list")

        if book.status != "voting":
            messages.warning(request, "This book is not in the voting stage.")
            return redirect("books:book_list")

        book.status = "reading"
        book.save()

        group, created = ReadingGroup.objects.get_or_create(book=book)
        if not created:
            messages.warning(
                request,
                f"A reading group already exists for '{book.title}'."
                "Users can join manually.",
            )
        else:
            group.participants.set(book.votes.all())
            messages.success(
                request, f"Voting closed! '{book.title}' is now in reading status."
            )
        return redirect("books:group_detail", pk=group.pk)


class GroupDetailView(LoginRequiredMixin, DetailView):
    """
    Displays details about a reading group.
    """

    model = ReadingGroup
    template_name = "books/group_detail.html"
    context_object_name = "group"

    def get_object(self):
        """
        Retrieves the group based on the provided ID.
        """
        return get_object_or_404(ReadingGroup, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["completed_sprint_ids"] = set(
            SprintProgress.objects.filter(
                user=self.request.user, is_read=True
            ).values_list("sprint_id", flat=True)
        )

        return context


class JoinGroupView(LoginRequiredMixin, View):
    """
    User joins the reading group.
    """

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(ReadingGroup, pk=kwargs["pk"])

        if request.user.reading_groups.exists():
            messages.warning(
                request,
                "You are already in another reading group. "
                "Leave the current group first.",
            )
            return redirect("books:group_detail", pk=group.pk)

        if not group.is_active:
            messages.error(request, "This reading group is closed.")
            return redirect("books:group_detail", pk=group.pk)

        group.participants.add(request.user)
        messages.success(request, "You joined the reading group.")
        return redirect("books:group_detail", pk=group.pk)


class LeaveGroupView(LoginRequiredMixin, View):
    """
    User leaves the reading group.
    """

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(ReadingGroup, pk=kwargs["pk"])

        if request.user not in group.participants.all():
            messages.warning(request, "You are not a part of this group.")
            return redirect("books:group_detail", pk=group.pk)

        group.participants.remove(request.user)
        messages.success(request, "You left the reading group.")
        return redirect("books:group_list")


class GroupListView(LoginRequiredMixin, ListView):
    """
    Displays a list of all active reading groups.
    """

    model = ReadingGroup
    template_name = "books/group_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        """
        Returns only active groups and precomputes participant count.
        """
        return (
            ReadingGroup.objects.filter(is_active=True)
            .select_related("book")
            .annotate(participant_count=Count("participants"))
        )


class ReadingSprintDetailView(LoginRequiredMixin, DetailView):
    model = ReadingSprint
    template_name = "books/sprint_detail.html"
    context_object_name = "sprint"

    def get_context_data(self, **kwargs):
        """
        Passes information if the user has completed this sprint.
        """
        context = super().get_context_data(**kwargs)
        sprint = self.object

        context["sprint_read"] = SprintProgress.objects.filter(
            user=self.request.user, sprint=sprint, is_read=True
        ).exists()

        return context


class ReadingSprintCreateView(AdminRequiredMixin, CreateView):
    model = ReadingSprint
    form_class = ReadingSprintForm
    template_name = "books/sprint_form.html"

    def form_valid(self, form):
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(ReadingGroup, id=group_id)
        sprint = form.save(commit=False)
        sprint.group = group
        sprint.save()
        messages.success(self.request, "Reading sprint created successfully.")
        return redirect("books:group_detail", pk=group.id)


class ReadingSprintUpdateView(AdminRequiredMixin, UpdateView):
    model = ReadingSprint
    form_class = ReadingSprintForm
    template_name = "books/sprint_form.html"

    def form_valid(self, form):
        sprint = form.save()
        messages.success(self.request, "Reading sprint updated successfully.")
        return redirect("books:sprint_detail", pk=sprint.id)


class ReadingSprintDeleteView(AdminRequiredMixin, DeleteView):
    model = ReadingSprint
    template_name = "books/sprint_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "books:sprint_list", kwargs={"group_id": self.object.group.id}
        )


class MarkSprintAsReadView(LoginRequiredMixin, View):
    """
    Allows a user to mark a reading sprint as completed.
    """

    def post(self, request, *args, **kwargs):
        sprint_id = kwargs["sprint_id"]
        group_id = kwargs["group_id"]
        sprint = get_object_or_404(ReadingSprint, id=sprint_id)

        # Check if user is a participant of the group
        if request.user not in sprint.group.participants.all():
            messages.error(request, "You are not a member of this reading group.")
            return redirect("books:sprint_detail", pk=sprint_id)

        progress, created = SprintProgress.objects.get_or_create(
            user=request.user,
            sprint=sprint,
        )

        if not progress.is_read:
            progress.is_read = True
            progress.completed_at = timezone.now()
            progress.save()
            messages.success(
                request, "You have successfully marked this sprint as read."
            )
        else:
            messages.info(request, "You have already marked this sprint as read.")

        return redirect("books:group_detail", pk=group_id)


class SprintIdeaCreateView(LoginRequiredMixin, View):
    """
    Each participant must add at least one idea for a sprint.
    """

    def get(self, request, sprint_id):
        form = SprintIdeaForm()
        return render(
            request, "books/idea_form.html", {"form": form, "sprint_id": sprint_id}
        )

    def post(self, request, sprint_id):
        sprint = get_object_or_404(ReadingSprint, id=sprint_id)

        if request.user not in sprint.group.participants.all():
            messages.error(request, "You are not in this group!")
            return redirect("books:sprint_detail", pk=sprint_id)

        form = SprintIdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.sprint = sprint
            idea.user = request.user
            idea.save()
            messages.success(request, "Your idea has been added!")
        else:
            messages.error(request, "Invalid form data.")
        return redirect("books:sprint_detail", pk=sprint_id)


class IdeaDiscussionCreateView(LoginRequiredMixin, View):
    """
    Adds a comment under a specific sprint idea.
    """

    def post(self, request, idea_id):
        idea = get_object_or_404(SprintIdea, id=idea_id)

        if request.user not in idea.sprint.group.participants.all():
            messages.error(request, "You are not in this group!")
            return redirect("books:sprint_detail", pk=idea.sprint.id)

        form = IdeaDiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.idea = idea
            discussion.user = request.user
            discussion.save()
            messages.success(request, "Comment added.")
        else:
            messages.error(request, "Invalid form data.")
        return redirect("books:sprint_detail", pk=idea.sprint.id)
