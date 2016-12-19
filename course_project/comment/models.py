from django.db import models
from django.utils import timezone

from personal_page.models import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=512)
    comment_text = models.TextField(max_length=1000, default=None)
    pub_date = models.DateTimeField(auto_now=True)

