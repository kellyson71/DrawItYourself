from django.urls import path
from .views import drawings_list, create_post

urlpatterns = [
    path('', drawings_list, name="main-page"),
    path('post/create/', create_post, name="create-post-page")
]