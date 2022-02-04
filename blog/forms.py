from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Profile


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "3"}), help_text="your comment here"
    )

    class Meta:
        model = Comment
        fields = ["comment"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["email", "bio", "image"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
