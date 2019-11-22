from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Post(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now = True)
    finished = models.DateTimeField(default = timezone.now())

    def __str__(self):
        return "{} by {}".format(self.name,self.author.username)

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE)
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return "Comment by {} to post {}".format(self.author.username,self.post.id)

class Share(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE)
    with_user = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return "{} shared with {}".format(self.post.id,self.with_user.username)