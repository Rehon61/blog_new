from django.shortcuts import render, HttpResponse, get_object_or_404
from .dataset import dataset
from .models import Post, Tag, Category
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .templatetags.md_to_html import markdown_to_html

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
    {"name": "Добавить пост", "alias": "add_post"}
]


def blog(request) -> HttpResponse:

    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(text__icontains=search_query).filter(status='published').order_by('-created_at')

    else:
        posts = Post.objects.filter(status='published').order_by('-created_at')

    context = {
        'posts': posts,
        'menu': menu,
        'page_alias': 'blog'
    }
    return render(request, 'blog_app/blog.html', context=context)


def post_by_slug(request, post_slug) -> HttpResponse:

    post = get_object_or_404(Post, slug=post_slug)
    context = {
        "post": post,
        "menu": menu,
        "page_alias": "blog"
    }

    return render(request, 'blog_app/post_detail.html', context=context, status=200)


def index(request) -> HttpResponse:
    context = {
        'menu': menu,
        'page_alias': 'main'
    }
    return render(request, 'index.html', context=context)


def about(request) -> HttpResponse:
    context = {
        'menu': menu,
        'page_alias': 'about'
    }
    return render(request, 'about.html', context=context)


def add_post(request):
    context = {
        'menu': menu,
        'page_alias': 'add_post'
    }

    # Если запрос типа GET - вернем страничку с формой добавления поста
    if request.method == "GET":
        return render(request, 'blog_app/add_post.html', context=context)

    # Если запрос типа POST - форма была отправлена и мы можем добавить пост
    elif request.method == "POST":

        title = request.POST['title']
        text = request.POST['text']
        tags = request.POST['tags']

        if Post.objects.filter(title=title).exists():
            context.update({'message': 'Такой заголовок уже существует!'})
            return render(request, 'blog_app/add_post.html', context=context)

        user = request.user

        if title and text and tags:
            post = Post.objects.create(
                title=title,
                text=text,
                author=user
            )
            tag_list = [tag.strip().lower().replace(' ', '_') for tag in tags.split(',') if tag.strip()]
            for tag_name in tag_list:
                tag = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            context.update({'message': 'Пост успешно добавлен!'})
            # return redirect( 'post_by_slug', post_slug=post.slug)
        else:
            context.update({'message': 'Заполните все поля!'})
            return render(request, 'blog_app/add_post.html', context=context)

    return render(request, 'blog_app/add_post.html', context=context)


def posts_by_tag(request, tag):
    """
    Функция представления для отображения страницы постов с определенным тегом.
    """
    context = {
        'posts': Post.objects.filter(tags__slug=tag),
        'menu': menu,
        'page_alias': 'blog'
    }
    return render(request, 'blog_app/blog.html', context=context)

def posts_by_category(request, category):
    context = {
        'posts': Category.objects.get(slug=category).posts.all(),
        'menu': menu,
        'page_alias': 'blog'
    }
    return render(request, 'blog_app/blog.html', context=context)

#@csrf_exempt
def preview_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        html = markdown_to_html(text)
        return JsonResponse({"html": html})
