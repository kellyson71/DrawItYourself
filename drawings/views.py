import json
from django.forms import inlineformset_factory
from django.shortcuts import render
from .models import Post, PostItem
from .forms import CreatePostForm

# Create your views here.
def drawings_list(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'index.html', context)

def create_post(request):
    PostItemFormSet = inlineformset_factory(Post, PostItem, fields=('image', 'image_legend'), extra=1)
    post_form = CreatePostForm()
    postitem_formset = PostItemFormSet(queryset=Post.objects.none())

    return render(request, 'create_post.html', { 'post_form': post_form, 'postitem_formset': postitem_formset })