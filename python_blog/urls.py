from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),

    #Через include подключим blog_app.urls
    path('', include('blog_app.urls')),

]
