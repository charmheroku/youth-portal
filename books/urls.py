from django.urls import path
from .views import (
    CreateReadingGroup,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    GroupDetailView,
    GroupListView,
    JoinGroupView,
    LeaveGroupView,
    ToggleVoteView,
)

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("create/", BookCreateView.as_view(), name="book_create"),
    path("<int:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
    path("vote/<int:pk>/", ToggleVoteView.as_view(), name="toggle_vote"),
    path(
        "finalize-voting/<int:pk>/",
        CreateReadingGroup.as_view(),
        name="finalize_voting",
    ),
    path("group/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("group/<int:pk>/join/", JoinGroupView.as_view(), name="join_group"),
    path("group/<int:pk>/leave/", LeaveGroupView.as_view(), name="leave_group"),
    path("groups/", GroupListView.as_view(), name="group_list"),
]
