import json
from django.forms import inlineformset_factory
from django.shortcuts import render
from .models import Post, PostItem, Favorite, Like, Comment
from .forms import CreatePostForm
from users.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from users.models import UserFollow  # Adicionar esta importação

PostItemFormSet = inlineformset_factory(Post, PostItem, fields=('image', 'image_legend'), extra=1)
POSTS_PER_PAGE = 3

def drawings_list(request):
    tab = request.GET.get('tab', 'all')
    
    if tab == 'following' and request.user.is_authenticated:
        following = UserFollow.objects.filter(follower=request.user).values_list('following', flat=True)
        all_posts = Post.objects.filter(author__in=following)
    elif tab == 'favorites' and request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('post', flat=True)
        all_posts = Post.objects.filter(id__in=favorites)
    else:
        all_posts = Post.objects.all()
        
    all_posts = all_posts.annotate(
        like_count=Count('like'),
        comment_count=Count('comment')
    ).order_by('-created_at')
    
    # Buscar posts populares separadamente - modificado para sempre trazer os dados
    trending_posts = Post.objects.annotate(
        like_count=Count('like')
    ).order_by('-like_count', '-created_at')[:5]
    
    paginator = Paginator(all_posts, POSTS_PER_PAGE)
    page = request.GET.get('p', 1)

    try:
        posts = paginator.get_page(page)
    except:
        posts = paginator.get_page(1)

    # Inicializar contagens mesmo para usuários não autenticados
    for post in posts:
        post.comments = Comment.objects.filter(post=post).select_related('user').order_by('-created_at')[:3]
        post.like_count = Like.objects.filter(post=post).count()
        post.comment_count = Comment.objects.filter(post=post).count()
        if request.user.is_authenticated:
            post.is_favorited = Favorite.objects.filter(user=request.user, post=post).exists()
            post.is_liked = Like.objects.filter(user=request.user, post=post).exists()
        else:
            post.is_favorited = False
            post.is_liked = False

    # Mesmo tratamento para trending_posts
    for post in trending_posts:
        post.like_count = Like.objects.filter(post=post).count()
        post.comment_count = Comment.objects.filter(post=post).count()

    # Adicionar informação de following para cada post
    for post in posts:
        if request.user.is_authenticated:
            post.is_following = UserFollow.objects.filter(
                follower=request.user,
                following=post.author
            ).exists()
        else:
            post.is_following = False

    context = {
        'posts': posts,
        'page': page,
        'trending_posts': trending_posts,
        'active_tab': tab
    }

    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        print(form.errors)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)

            return redirect('login')  # Redireciona para a página de login após o cadastro
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})
    
@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        post_form = CreatePostForm(request.POST)
        postitem_formset = PostItemFormSet(request.POST, request.FILES)
        
        if post_form.is_valid() and postitem_formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            
            post_items = postitem_formset.save(commit=False)
            for post_item in post_items:
                post_item.post = post
                post_item.save()
                
            # return redirect('post_detail', post_id=post.id)
            return redirect('main-page')
    else:
        post_form = CreatePostForm()
        postitem_formset = PostItemFormSet(queryset=PostItem.objects.none())

    context = {
        'post_form': post_form,
        'postitem_formset': postitem_formset
    }
    
    return render(request, 'create_post.html', context)

@login_required(login_url='login')
def delete_post(request, post_id):
    Post.objects.get(id=post_id).delete()

    return redirect('main-page')

@login_required(login_url='login')
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post_form = CreatePostForm(request.POST, instance=post)
        postitem_formset = PostItemFormSet(request.POST, request.FILES, instance=post)
        
        if post_form.is_valid() and postitem_formset.is_valid():
            post_form.save()
            post_items = postitem_formset.save(commit=False)

            for post_item in post_items:            
                post_item.save()
                
            return redirect('main-page')
    else:
        post_items = PostItem.objects.filter(post=post)

        post_form = CreatePostForm(instance=post)
        postitem_formset = PostItemFormSet(instance=post)
    
    context = {
        'post_form': post_form,
        'postitem_formset': postitem_formset
    }

    return render(request, 'create_post.html', context)

@login_required(login_url='login')
def profile_view(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'user': request.user,
        'posts': user_posts,
    }
    return render(request, 'profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        post=post
    )
    
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True
        
    return JsonResponse({
        'is_favorited': is_favorited
    })

@login_required(login_url='login')
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('post')
    favorites_posts = [favorite.post for favorite in favorites]
    
    paginator = Paginator(favorites_posts, POSTS_PER_PAGE)
    page = request.GET.get('p', 1)
    
    try:
        posts = paginator.get_page(page)
    except:
        posts = paginator.get_page(1)
    
    for post in posts:
        post.is_favorited = True
    
    context = {
        'posts': posts,
        'page': page
    }
    
    return render(request, 'favorites.html', context)

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(post=post, user=request.user).first()
    
    if like:
        like.delete()
        is_liked = False
    else:
        Like.objects.create(post=post, user=request.user)
        is_liked = True
        
    return JsonResponse({'is_liked': is_liked})

@login_required(login_url='login')
def likes_view(request):
    likes = Like.objects.filter(user=request.user).select_related('post')
    liked_posts = [like.post for like in likes]
    
    paginator = Paginator(liked_posts, POSTS_PER_PAGE)
    page = request.GET.get('p', 1)
    
    try:
        posts = paginator.get_page(page)
    except:
        posts = paginator.get_page(1)
    
    for post in posts:
        post.is_liked = True
    
    context = {
        'posts': posts,
        'page': page
    }
    
    return render(request, 'likes.html', context)

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                created_at=timezone.now()
            )
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    
    for post in user_posts:
        post.like_count = Like.objects.filter(post=post).count()
        post.comment_count = Comment.objects.filter(post=post).count()
        if request.user.is_authenticated:
            post.is_favorited = Favorite.objects.filter(user=request.user, post=post).exists()
            post.is_liked = Like.objects.filter(user=request.user, post=post).exists()
        else:
            post.is_favorited = False
            post.is_liked = False
    
    context = {
        'profile_user': user,
        'posts': user_posts,
        'posts_count': user_posts.count(),
        'likes_count': Like.objects.filter(post__author=user).count(),
    }
    return render(request, 'user_detail.html', context)
