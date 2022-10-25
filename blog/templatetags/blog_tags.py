import markdown
from blog.models import Post
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

register = template.Library()


#  note diff with inclusinon_tag which processes the data and returns a rendered template
# * optionally pass in name simple_tag(name="my_name") to override function name and use that as template tag name
@register.simple_tag
def total_posts():
    """Count total number of published posts"""

    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count: int = 5):
    """Show the latests posts ordered by publish date"""
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.inclusion_tag("blog/post/most_commented.html")
def show_most_commented_posts(count: int = 5, comment_count: int = 2):
    """Show posts with most comments"""
    most_commented = Post.published.filter(comments__gt=comment_count).order_by(
        "-publish"
    )[:count]
    return {"most_commented": most_commented}


#  diff impl
# better approach
@register.simple_tag
def get_most_commented(count: int = 5):
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


# BUG: fails to render markdown content added via the admin
@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
