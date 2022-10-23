from django.urls import path
from blog import views

# define app namespace to use in URLs when calling
app_name = 'blog'

urlpatterns = [

    # path('', views.post_list, name='post_list'),  # using a function
    path('', views.PostListView.as_view(),
         name='post_list'),  # using a class
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
