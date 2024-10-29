from django.contrib import admin
from django.urls import path, include
from blog_app.views import index, about
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="main"),
    path("about/", about, name="about"),

    # Через include подключим blog_app.urls
    # http://127.0.0.1:8000/blog/post/django-osnovnye-komandy
    # path('blog/', include('blog_app.urls')),

    # http://127.0.0.1:8000/post/django-osnovnye-komandy
    path('blog/', include('blog_app.urls')),
    path('users/', include('users.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns