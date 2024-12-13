from django.forms import ModelForm, CharField, PasswordInput, ValidationError
from users.models import User

class SignUpForm(ModelForm):
    confirm_password = CharField(max_length=100, widget=PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            return ValidationError('The passwords doesn\'t match.')
        
        del cleaned_data['confirm_password']

        return cleaned_data