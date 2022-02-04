from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CommentForm, ProfileForm, UserUpdateForm
from .models import Comment, Post, Profile


class PostListView(ListView):
    """
    creates a list view for posts
    """

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "post_list"


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    creates a form view for posts
    """

    model = Post
    fields = ["title", "body"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        """track the user that created a post"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    creates delete view for posts
    """

    model = Post
    success_url = reverse_lazy("post-list")
    template_name = "blog/post_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    creates update view for posts
    """

    model = Post
    fields = ["title", "body"]


class PostDetailView(View):
    """
    alternative comment view
    """

    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def get(self, request, pk, *args, **kwargs):
        form = self.form_class()
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        context = {
            "form": form,
            "post": post,
            "comments": comments,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, pk=pk)
        context = {
            "form": form,
        }
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.owner = self.request.user
            comment.save()
            messages.success(request, f"Comment successfull!")
            return redirect("post-detail", pk=post.pk)
        return render(request, self.template_name, context)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """
    creates a delete view for posts
    """

    model = Comment
    fields = ["comment"]

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})


class ProfileView(View):
    form_class = UserUpdateForm
    form_class1 = ProfileForm
    template_name = "blog/profile.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        u_form = self.form_class(instance=request.user)
        p_form = self.form_class1(instance=request.user.profile)
        context = {
            "u_form": u_form,
            "p_form": p_form,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        u_form = self.form_class(request.POST, instance=request.user)
        p_form = self.form_class1(
            request.POST, request.FILES, instance=request.user.profile
        )
        context = {
            "u_form": u_form,
            "p_form": p_form,
        }
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")

        return render(request, self.template_name, context)


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-created")


class UserCommentListView(ListView):
    model = Comment
    template_name = "blog/user_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Comment.objects.filter(owner=user).order_by("-created")


class UserProfileListView(ListView):
    model = Profile
    template_name = "blog/user_profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Comment.objects.filter(owner=user)


class SearchResultsView(ListView):
    model = Post
    template_name = "blog/search.html"
    context_object_name = "searches"

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query != None:
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
            return object_list


class AboutPageView(TemplateView):
    template_name = "about.html"
