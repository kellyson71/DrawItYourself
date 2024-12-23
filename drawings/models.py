from django.db import models

from users.models import User, UserFollow  # Adicionar UserFollow aqui

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    REGULAR = 'REGULAR'
    COMIC = 'COMIC'
    POST_TYPES = {
        REGULAR: 'REGULAR',
        COMIC: 'COMIC'
    }

    type = models.CharField(choices=POST_TYPES, max_length=30)
    tags = models.ManyToManyField(Tag)

    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_drawing_pages(self):
        if self.type == 'REGULAR':
            return PostItem.objects.filter(post=self)
        else:
            return ComicPage.objects.filter(post=self).order_by('page_order')

    def is_liked_by(self, user):
        return Like.objects.filter(post=self, user=user).exists()

    def is_following(self):
        if not hasattr(self, '_current_user'):
            return False
        
        if not hasattr(self, '_is_following'):
            self._is_following = UserFollow.objects.filter(
                follower=self._current_user,
                following=self.author
            ).exists()
        return self._is_following

    def __str__(self) -> str:
        return f"{self.author} | {self.title}"

class PostItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_legend = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='post-items/')

    def get_image_path(self):
        return "A"

    def __str__(self):
        return f"{self.post.author} | {self.post.title} | {self.image_legend}"

class ComicPage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comic-page/')
    page_order = models.IntegerField()

    def __str__(self):
        return f"{self.post.author} | {self.post.title} | {self.page_order}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.post.title} | {self.user} - {self.content}"

class Favorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} | {self.user}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} | {self.user}"