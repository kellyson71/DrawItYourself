from django.db import models
from django.contrib.auth.models import User as AuthUser  # Adicione esta linha

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return self.username

class Message(models.Model):
    sender = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField()
    is_read = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content}"

class MessageImage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="message-images/")
    
    def __str__(self):
        return f"{self.message.sender}: {self.message.content}"

class UserFollow(models.Model):
    follower = models.ForeignKey(AuthUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(AuthUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"