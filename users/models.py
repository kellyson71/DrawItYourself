from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class CustomManager(UserManager):
    def create_user(self, username, email, password, **extra_fields):
        user = User.objects.create(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        user = User.objects.create(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user

class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/')

    REQUIRED_FIELDS = ['email']

    objects = CustomManager()

    def __str__(self):
        return self.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content}"

class MessageImage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="message-images/")
    
    def __str__(self):
        return f"{self.message.sender}: {self.message.content}"