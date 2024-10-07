from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from unidecode import unidecode


class Post(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик'),
    )
    title = models.CharField(max_length=300, unique=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    slug = models.SlugField(unique=True, verbose_name='Адрес страницы')
    author = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey('Category', related_name='posts', null=True, default=None, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True, verbose_name='Теги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    cover_image = models.ImageField(blank=True, null=True, verbose_name='Обложка', upload_to='media/images/')

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("post_by_slug", args=[str(self.slug)])
        # return f"blog/{self.slug}/view/ # Это 2-й вариант работы с адресами в Django

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматической генерации slug
        """
        slug = slugify(unidecode(self.title))
        self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('posts_by_category', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        slug = slugify(unidecode(self.name))
        self.slug = slug
        super().save(*args, **kwargs)



class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower().replace(' ', '_')
        slug = slugify(unidecode(self.name))
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'#{self.name}'

    def get_absolute_url(self):
        """
        Возвращает маршрут posts_by_tag
        """
        url = reverse('posts_by_tag', args=[str(self.slug)])
        return url


class Comment(models.Model):

    STATUS_CHOICES = (
        ('unchecked', 'Не проверен'),
        ('accepted', 'Проверен'),
        ('rejected', 'Отклонен'),
    )
    text = models.TextField(verbose_name='Текст комментария', max_length=2000)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='unchecked')


    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')


