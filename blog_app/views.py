from django.shortcuts import render, HttpResponse, get_object_or_404
from .dataset import dataset
from .models import Post, Tag, Category
from django.db.models import F,Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .templatetags.md_to_html import markdown_to_html
from .forms import CommentForm, CategoryForm, TagForm
from django.shortcuts import render, redirect
from .models import Post, Tag
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
    {"name": "Добавить пост", "alias": "add_post"}
]


def blog(request) -> HttpResponse:
    search_query = request.GET.get("search", "")
    search_category = request.GET.get("search_category")
    search_tag = request.GET.get("search_tag")
    search_comments = request.GET.get("search_comments")
    page_number = request.GET.get('page', 1) # Получаем номер страницы из URL-параметра

    posts = Post.objects.prefetch_related('tags').select_related('author').select_related('category').filter(status="published")

    if search_query:
        query = Q(title__icontains=search_query) | Q(text__icontains=search_query)

        if search_category:
            query |= Q(category__name__icontains=search_query)

        if search_tag:
            query |= Q(tags__name__icontains=search_query)

        if search_comments:
            query |= Q(comment__text__icontains=search_query)

        posts = posts.filter(query)

    posts = posts.distinct().order_by("-created_at")

    paginator = Paginator(posts,2) # первый аргумент - кверисет, второй - сколько объектов на странице

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1) # Если параметр page не число, показываем первую страницу
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # Если страница

    context = {"page_obj": posts, "menu": menu, "page_alias": "blog"}
    return render(request, 'blog_app/blog.html', context=context)


def post_by_slug(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():

                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.status = 'unchecked'
                comment.save()
                messages.success(request, 'Ваш комментарий находится на модерации.')
                return redirect('post_by_slug', post_slug=post_slug)
        else:
            messages.error(request, 'Для добавления комментария необходимо войти в систему.')
            return redirect('login')
    else:
        form = CommentForm()

    comments_list = post.comments.filter(status='accepted').order_by('created_at')
    paginator = Paginator(comments_list, 20)  # 5 комментариев на страницу
    page_number = request.GET.get('page')

    try:
        comments_page = paginator.page(page_number)
    except PageNotAnInteger:
        comments_page = paginator.page(1)
    except EmptyPage:
        comments_page = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'form': form,
        'comments': comments_page,
    }

    return render(request, 'blog_app/post_detail.html', context)


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
            tag_list = [tag.strip().lower().replace(' ', '_')
                        for tag in tags.split(',')
                        if tag.strip()
                        ]

            for tag_name in tag_list:
                tag,created = Tag.objects.get_or_create(name=tag_name)
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

def add_category(request):
    context = {"menu": menu}

    if request.method == "GET":
        form = CategoryForm()
        context['form'] = form
        return render(request,'blog_app/add_category.html', context)

    elif request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # if Category.objects.filter(name=form.cleaned_data['name']).exists():
            #     pass

            name = form.cleaned_data['name']
            Category.objects.create(name=name)
            context['message'] = f'Категория {name} успешно добавлена!'
            return render(request, "blog_app/add_category.html", context)
        context['form'] = form
        return render(request, "blog_app/add_category.html", context)


def add_tag(request):

    context = {'menu': menu}

    if request.method == 'GET':
        form = TagForm()
        context['form'] = form
        return render(request, 'blog_app/add_tag.html', context)

    elif request.method =='POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['name']
            context['message'] = f'Тег {name} успешно добавлен!'
            return render(request, 'blog_app/add_tag.html', context)
        context['form'] = form
        return render(request, 'blog_app/add_tag.html', context)