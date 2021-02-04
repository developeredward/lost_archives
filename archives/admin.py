from django.contrib import admin
from .models import Author, Category, Post, Comment
from embed_video.admin import  AdminVideoMixin


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Author, MyModelAdmin)
admin.site.register(Category, MyModelAdmin)
admin.site.register(Post, MyModelAdmin)
admin.site.register(Comment, MyModelAdmin)
