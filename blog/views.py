from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from blog.models import Post

# Create your views here.


class PostListView(ListView):
    # alternative syntax to get all posts instead of just published posts
    # model = Post
    queryset = Post.published.all()
    # default without specification is object_list
    # ? is this equivalent to post_list
    context_object_name = 'posts'
    paginate_by = 3
    # default without specification is blog/post_list.html
    template_name = 'blog/post/list.html'


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


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
