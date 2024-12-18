from django.contrib import admin
from .models import User, Message, MessageImage, UserFollow

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_fields = ['username', 'email']

@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    UserFollow = ['follower', 'following']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['content', 'sender', 'receiver']
    search_fields = ['sender', 'receiver']
    list_filter = ['sender', 'receiver']

@admin.register(MessageImage)
class MessageImageAdmin(admin.ModelAdmin):
    list_display = ['message']
    search_fields = ['message']