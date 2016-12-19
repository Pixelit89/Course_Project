from django.contrib import admin
from .models import Account, Post
admin.site.register((Account, Post,))
