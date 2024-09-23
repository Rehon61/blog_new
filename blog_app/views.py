from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render
from .dataset import dataset

def index(request):
    context = {
        'posts': dataset
    }
    return render(request, 'blog_app/index.html', context=context)


def post_by_slug(request, post_slug):
    post = [post for post in dataset if post['slug'] == post_slug]
    if not post:
        return HttpResponse('404 - Пост не найден', status=404)
    else:
        return render(request, 'blog_app/post_detail.html', context=post[0], status=200)