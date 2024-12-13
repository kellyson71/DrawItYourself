from django.forms import ModelForm, TextInput, RadioSelect, Textarea, FileInput, HiddenInput
from .models import Post, PostItem
from django import forms

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
        fields = ['image', 'image_legend', 'id']
        
        widgets = {
            'image': FileInput(attrs={'class': 'image-input'}),
            'image_legend': TextInput(attrs={ 'placeholder': 'Legenda' }),
            'id': HiddenInput()
        }
