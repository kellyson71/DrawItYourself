from django.db import models

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