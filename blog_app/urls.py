from django.urls import path
from .views import post_by_slug, blog, add_post, posts_by_tag, posts_by_category

urlpatterns = [
    path("<slug:post_slug>/view/", post_by_slug, name="post_by_slug"),
    path("", blog, name="blog"),
    path("add/", add_post, name="add_post"),
    # Посты по тегам
    path('tag/<slug:tag>/', posts_by_tag, name='posts_by_tag'),
    path('category/<slug:category>/', posts_by_category, name='posts_by_category'),
]