from django.urls import path
from .views import post_by_slug, blog, add_post, posts_by_tag, posts_by_category, preview_post, add_category, add_tag, update_category, update_post

urlpatterns = [
    path("<slug:post_slug>/view/", post_by_slug, name="post_by_slug"),
    path("", blog, name="blog"),

    path("add_post/", add_post, name="add_post"),
    path("update_post/<slug:post_slug>/", update_post, name="update_post"),
    path("add_category/", add_category, name="add_category"),
    path('update_category/<slug:category_slug>/', update_category, name='update_category'),
    path("add_tag/", add_tag, name="add_tag"),

    path('tag/<slug:tag>/', posts_by_tag, name='posts_by_tag'),
    path('category/<slug:category>/', posts_by_category, name='posts_by_category'),
    path('preview/', preview_post, name='preview_post'),
]