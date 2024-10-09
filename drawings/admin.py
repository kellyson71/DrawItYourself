from django.contrib import admin
from .models import Tag, PostItem, Comment, Favorite, ComicPage, Like, Post

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'type']
    search_fields = ['title', 'author']
    list_filter = ['author', 'type', 'tags']

@admin.register(PostItem)
class PostItemAdmin(admin.ModelAdmin):
    list_display = ['image_legend', 'post']
    search_fields = ['image_legend', 'post']

@admin.register(ComicPage)
class ComicPageAdmin(admin.ModelAdmin):
    list_display = ['page_order', 'post']
    search_fields = ['post']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'content']
    search_fields = ['post', 'user']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
    search_fields = ['post', 'user']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
    search_fields = ['post', 'user']