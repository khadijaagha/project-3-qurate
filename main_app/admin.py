from django.contrib import admin
from .models import Profile, Post, LikePost

# Register you models here
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)