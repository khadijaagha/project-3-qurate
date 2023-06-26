from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

class Post(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField(blank=True)
    description = models.CharField(max_length=300, blank=True)
    tags = models.CharField(max_length=30, blank=True)
    likes = models.IntegerField(default=0)
    # likes = models.ManyToManyField(Like, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('user_feed')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=500)
    likes = models.IntegerField(default=0)
    # likes = models.ManyToManyField(Like, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post_likes = models.ManyToManyField(Post, related_name="posts_liked", blank=True)
    comment_likes = models.ManyToManyField(Comment, related_name="comments_liked", blank=True)
    follows = models.ManyToManyField('self', related_name='followed_by', blank=True, symmetrical=False)
    def __str__(self):
        return f'{self.user.username} - user.id: ({self.user_id}) profile id: ({self.id})'

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class MessageRoom(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='message_room')

    def __str__(self):
        return f'{self.name}'

class Message(models.Model):
    body = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'{self.sender.username} - "{self.body}" - {self.timestamp} - {self.room}'