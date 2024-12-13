import json
from django.forms import inlineformset_factory
from django.shortcuts import render
from .models import Post, PostItem
from users.models import User
from .forms import CreatePostForm
from users.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.models import User
from django.contrib.auth.forms import UserCreationForm

PostItemFormSet = inlineformset_factory(Post, PostItem, fields=('image', 'image_legend'), extra=1)

# Create your views here.
def drawings_list(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
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
    
@login_required
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

def delete_post(request, post_id):
    Post.objects.get(id=post_id).delete()

    return redirect('main-page')

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