from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('message/<str:username>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('chat/<str:username>/', views.chat_detail, name='chat_detail'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('following/', views.following_artists, name='following_artists'),
]
