from typing import AnyStr

from django.urls import path
from blog_app.views import index,post_by_slug

urlpatterns: list[AnyStr] = [
    path('post/<slug:post_slug>', post_by_slug, name='post_by_slug'),
    path('',index),
]