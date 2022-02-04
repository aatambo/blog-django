from django.conf import settings
from django.db import models
from django.urls import reverse
from PIL import Image


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
     updating ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    """
    creates a model for posts
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    """
    creates a model for comments
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Comment by {self.owner} on {self.post}"


class Profile(models.Model):
    """
    create a model for user profile
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default="user.png", upload_to="uploads")
    bio = models.TextField(default="no bio...", max_length=254)
    email = models.EmailField(blank=True, help_text="Secondary email.")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
