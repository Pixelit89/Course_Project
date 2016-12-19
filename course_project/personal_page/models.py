from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Account(User):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    friends = models.ManyToManyField('self', related_name='friends', blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    account = models.ForeignKey(Account)
    post_name = models.CharField(max_length=512, default='Post name')
    post = models.TextField(default='Empty post')
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post


class LikeCollector(models.Model):
    post = models.ManyToManyField(Post)
    who_liked = models.IntegerField()
    post_liked = models.IntegerField()
