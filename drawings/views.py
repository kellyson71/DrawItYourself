import json
from django.forms import inlineformset_factory
from django.shortcuts import render
from .models import Post, PostItem
from .forms import CreatePostForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Favorite

POSTS_PER_PAGE = 3

def drawings_list(request):
    all_posts = Post.objects.all().order_by('-created_at')  # Ordenar por data de criação
    paginator = Paginator(all_posts, POSTS_PER_PAGE)

    page = request.GET.get('p', 1)

    try:
        posts = paginator.get_page(page)
    except:
        page = 1
        posts = paginator.get_page(1)

    # Adicionar informação de favoritos para cada post
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('post_id', flat=True)
        for post in posts:
            post.is_favorited = post.id in favorites

    context = {
        'posts': posts,
        'page': page
    }

    return render(request, 'index.html', context)


from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Erro em {field}: {error}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})
    
@login_required(login_url='login')
def create_post(request):
    PostItemFormSet = inlineformset_factory(Post, PostItem, fields=('image', 'image_legend'), extra=1)
    
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        # postitem_formset = PostItemFormSet(request.POST, request.FILES)
        
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            
            # post_items = postitem_formset.save(commit=False)
            # for post_item in post_items:
            #     post_item.post = post
            #     post_item.save()
                
            # return redirect('post_detail', post_id=post.id)
            return redirect('main-page')
    else:
        post_form = PostForm()
        # postitem_formset = PostItemFormSet(queryset=PostItem.objects.none())
    
    return render(request, 'create_post.html', {
        'post_form': post_form
        # 'postitem_formset': postitem_formset
    })

@login_required(login_url='login')
def delete_post(request, post_id):
    Post.objects.get(id=post_id).delete()

    return redirect('main-page')

@login_required(login_url='login')
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        # postitem_formset = PostItemFormSet(request.POST, request.FILES)
        
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            
            # post_items = postitem_formset.save(commit=False)
            # for post_item in post_items:
            #     post_item.post = post
            #     post_item.save()
                
            # return redirect('post_detail', post_id=post.id)
            return redirect('main-page')
    else:
        post_form = PostForm(instance=post, initial={ 'image': post.image.url })
        # postitem_formset = PostItemFormSet(queryset=PostItem.objects.none())
    
    return render(request, 'create_post.html', {
        'post_form': post_form
        # 'postitem_formset': postitem_formset
    })

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