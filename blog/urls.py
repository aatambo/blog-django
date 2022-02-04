from django.urls import path

from .views import (
    AboutPageView,
    CommentUpdateView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    ProfileView,
    SearchResultsView,
    UserCommentListView,
    UserPostListView,
    UserProfileListView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("add/", PostCreateView.as_view(), name="post-form"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<int:pk>/update", PostUpdateView.as_view(), name="post-update"),
    path("comment/<int:pk>", CommentUpdateView.as_view(), name="comment-update"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/<str:username>", UserProfileListView.as_view(), name="profile-user"),
    path("posts/<str:username>", UserPostListView.as_view(), name="posts"),
    path("comments/<str:username>", UserCommentListView.as_view(), name="comments"),
    path("search/", SearchResultsView.as_view(), name="search"),
    path("about/", AboutPageView.as_view(), name="about"),
]
