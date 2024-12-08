from django.urls import path
from .views import drawings_list, create_post
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', drawings_list, name="main-page"),
    path('post/create/', create_post, name="create-post-page"),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Substituir a linha antiga do logout
    path('signup/', views.signup, name='signup'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('profile/', views.profile_view, name='profile'),
    path('favorites/', views.favorites_view, name='favorites'),
]
