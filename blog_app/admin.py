from django.contrib import admin
from .models import Post, Tag,Category,Comment

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'created_at', 'updated_at')
#     search_fields = ('title', 'text')
#     prepopulated_fields = {'slug': ('title',)}
