from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    #! To reference following and followers, might have to use user.id
    # following_users = models.ManyToManyField(User)
    # follower_users = models.ManyToManyField(User)
    # followers = models.ManyToManyField('self', related_name='follower',blank=True)
    # following = models.ManyToManyField('self', related_name='following',blank=True)
    #! posts = models.ForeignKey()
    #! post_likes = models.ManyToManyField(Post, on_delete=models.DO_NOTHING)

class Follows(models.Model):
    # following_user_id = models.ManyToManyField(User)
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.DO_NOTHING)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.DO_NOTHING)


# class Tag(models.Model):
#     label = models.CharField(max_length=20)


class Post(models.Model):
    url = models.CharField(max_length=200)
    # url = models.ImageField()
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=300)
    # tags = models.ManyToManyField(Tag, on_delete=models.DO_NOTHING)
    # tags = models.ManyToManyField(Tag)
    tags = models.CharField(max_length=30)
    # likes = models.IntegerField()
    # ! This might be really slow, but I can only do it this way round as the Post class comes after the Profile class
    #? likes = models.ManyToManyField(Profile, on_delete=models.DO_NOTHING)
    likes = models.ManyToManyField(Profile)
    # ! End Note
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        pass 


class Comment(models.Model):
    # url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # parent = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    body = models.TextField(max_length=500)
    likes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Sub_Comment(Comment):
#     parent = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)