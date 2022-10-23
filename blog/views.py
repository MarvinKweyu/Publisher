from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post, Comments

# Create your views here.


class PostListView(ListView):
    # alternative syntax to get all posts instead of just published posts
    # model = Post
    queryset = Post.published.all()
    # default without specification is object_list
    # ? is this equivalent to post_list
    context_object_name = "posts"
    paginate_by = 3
    # default without specification is blog/post_list.html
    template_name = "blog/post/list.html"


# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3)  # 3 posts per paeg
#     page = request.GET.get('page')

#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # deliver the first page if hte page is not an integer
#         posts = paginator.page(1)
#     except EmptyPage:
#         # give the last page if the page is out of bounds
#         posts = paginator.page(paginator.num_pages)

#     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(
#         Post,
#         slug=post,
#         status="published",
#         publish__year=year,
#         publish__month=month,
#         publish__day=day,
#     )
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     comment_form = CommentForm()

#     if request.method == "POST":
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # create comment obj without saving to db
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post  # associate comment with post
#             new_comment.save()  # eventually save
#     return render(
#         request,
#         "blog/post/detail.html",
#         {
#             "post": post,
#             "comments": comments,
#             "new_comment": new_comment,
#             "comment_form": comment_form,
#         },
#     )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )


def post_share(request, post_id):
    # get post by id
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False
    form = EmailPostForm()
    if request.method == "POST":
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            # use get_absolute_url to build the complete URL including schema and host name
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{clean_data['name']} recommends you read {post.title}"
            from_email = "admin@publisher.com"
            message = f"Read {post.title} at {post_url} \n\n {clean_data['name']}'s comments: {clean_data['comments']}"
            # send mail
            send_mail(subject, message, from_email, [clean_data["to"]])
            sent = True

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
