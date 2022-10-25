from django.urls import path
from blog import views
from blog.feeds import LatestPostsFeed

# define app namespace to use in URLs when calling
app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),  # using a function
    # path("", views.PostListView.as_view(), name="post_list"),  # using a class
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    # use slug path converter to match param as lowercase string with ASCII plus hyphen and underscores
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
]
