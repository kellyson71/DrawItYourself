from django.forms import ModelForm, TextInput, RadioSelect, Textarea, FileInput
from .models import Post, PostItem
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'type', 'image'] 
        
        widgets = {
            'title': TextInput(attrs={ 'placeholder': 'Título', 'class': 'title' }),
            'description': Textarea(attrs={ 'placeholder': 'Descrição' }),
            'type': RadioSelect(choices=Post.POST_TYPES),
            'image': FileInput(attrs={ 'class': 'invisible', 'id': 'image-input' })
        }

class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'type']

        widgets = {
            'title': TextInput(attrs={ 'placeholder': 'Título', 'class': 'title' }),
            'description': Textarea(attrs={ 'placeholder': 'Descrição' }),
            'type': RadioSelect(choices=Post.POST_TYPES)
        }

class PostItemForm(ModelForm):
    class Meta:
        model = PostItem
        fields = ['image', 'image_legend']
        
        widgets = {
            'image': FileInput(),
            'image_legend': TextInput()
        }
