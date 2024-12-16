from django.forms import ModelForm, TextInput, RadioSelect, Textarea, FileInput, HiddenInput
from .models import Post, PostItem
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove as mensagens de validação
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        
    def _post_clean(self):
        super()._post_clean()
        # Remove as validações de senha
        self._errors.pop('password2', None)
