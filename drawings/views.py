import json
from django.forms import inlineformset_factory
from django.shortcuts import render
from .models import Post, PostItem
from .forms import CreatePostForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.shortcuts import get_object_or_404

# Create your views here.
def drawings_list(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'index.html', context)


from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para a página de login após o cadastro
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})
    
@login_required
def create_post(request):
    PostItemFormSet = inlineformset_factory(Post, PostItem, fields=('image', 'image_legend'), extra=1)
    
    if request.method == 'POST':
        post_form = CreatePostForm(request.POST, request.FILES)
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
    
    return render(request, 'create_post.html', {
        'post_form': post_form, 
        'postitem_formset': postitem_formset
    })