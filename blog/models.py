from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    """
    Stores a single post .related to :model: `auth.User`
    """

    STATUS_CHOICES = (("draft", "Draft"), ("published", "Published"))
    title = models.CharField(max_length=250)
    # only one post with a slug for a given date
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager
    tags = TaggableManager()

    class Meta:
        # recent posts appear first
        ordering = ("-publish",)
        # Todo: come back to see how
        # default_manager_name = PublishedManager

        def __str__(self):
            return self.title

    def get_absolute_url(self):
        """Access the full URL of a single post"""
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class Comments(models.Model):
    """Shows the views on a specific post. Relates to :model: `blog.Post`"""

    # let me get the comment of a post via comment.post or all comments of a post via post.comments.all()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    #  name of the user who created the comment
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
