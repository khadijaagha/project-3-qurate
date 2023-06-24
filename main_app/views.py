import uuid
import boto3
import os
import requests
import random
from . import urls
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Post, Comment, User, Message, MessageRoom
from .forms import UserCreationForm
from django_ratelimit.decorators import ratelimit

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# ! PAGES --------------------------
# @login_required
def user_feed(request):
    following_users = request.user.profile.follows.all()
    user_posts = Post.objects.filter(user__profile__in=following_users).order_by('created_at')
    
    return render(request, 'qurate/feed.html', {
        'title': 'Your Feed',
        'posts': user_posts
    })

def explore(request):
        posts = Post.objects.all().order_by('created_at')
        return render(request, 'qurate/explore.html', {
        'posts': posts,
        'title': 'Explore'
    })

# @ratelimit(key = ratelimitkey(user = 'user', rate = '10/s', method = ratelimit.ALL))
@ratelimit(key = 'ip', rate = '79/s', method = ratelimit.ALL)
def inspo(request):
    response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=True&q=')
    inspo_data = response.json()
    posts = []
    random_posts = inspo_data['objectIDs']
    random.shuffle(random_posts)
    idx = 0
    for post in random_posts:
        response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{post}')
        inspo = response.json()
        if inspo == {'message': 'Not a valid object'} or inspo['primaryImage'] == '' or inspo['title'] == 'Worker Shabti of Nauny' or len(inspo['title']) > 50:
            continue
        posts.append(inspo) 
        idx += 1
        if idx == 6:
            break
    return render(request, 'qurate/inspiration.html', {
        'inspo': posts,
        'title': 'Inspiration',
    })

# @login_required
def posts_detail(request, posts_id):

    return render(request, 'posts/detail.html', {

    })

# ! POSTS ------------------

class PostCreate(CreateView):
    model = Post
    fields = ['title', 'price', 'description', 'tags']

    def form_valid(self, form):
        form.instance.user = self.request.user
        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                post = form.save(commit=False)
                post.url = url
                post.save()
            except Exception as e:
                print('An error occurred uploading file to S3')
        return super().form_valid(form)
        




class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'price', 'description', 'tags']

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    # if request.method == 'POST':
    success_url = '/qurate'

# ! COMMENTS ---------------------

def add_comment(request, post_id):
    return render(request, 'posts/add_comment.html', {

    })


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment


# ! TAGS ----------------------
def tags_index(request, tags):
    posts = Post.objects.filter(tags=tags)
    return render(request, 'qurate/tags.html', {
        'title': '#' + tags,
        'posts': posts
    })



# ! USERS --------------------

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            following_users = request.user.profile.follows.all()
            user_posts = Post.objects.filter(user__profile__in=following_users).order_by('created_at')
            return redirect('user_feed')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def users_detail(request, user_id):
    profile = Profile.objects.get(id=user_id)
    user_posts = Post.objects.filter(user=user_id)
    post_count = Post.objects.filter(user=user_id).count();
    if profile.followed_by.filter(id=request.user.id).exists():
        is_following = True;
    else:
        is_following = False;
    return render(request, 'users/detail.html', {
        'profile': profile,
        'title': f"{profile.user}'s Pofile",
        'posts': user_posts,
        'post_count': post_count,
        'is_following': is_following
    })

def follow(request, user_id):
    profile = Profile.objects.get(id=user_id)
    user_posts = Post.objects.filter(user=user_id)
    post_count = Post.objects.filter(user=user_id).count();
    is_following = False
    if request.method == 'POST':
        if profile.followed_by.filter(id=request.user.id).exists():
            profile.followed_by.remove(request.user.profile)
            is_following = False
        else:
            profile.followed_by.add(request.user.profile)
            is_following = True
    return render(request, 'users/detail.html', {
        'profile': profile,
        'title': f"{profile.user}'s Profile",
        'posts': user_posts,
        'is_following': is_following,
        'post_count': post_count
    })


# ! SEARCH ----------------

def search(request):
    search_content = request.POST.get('search')
    tags = []
    users = []
    if search_content[0] == '#':
        no_hash = search_content.strip('#')
        tags = Post.objects.filter(tags__icontains=no_hash)
        print(f'tags {tags}')
    else:
        users = User.objects.filter(username__icontains=search_content)
        print(f'{users}')
    return render(request, 'qurate/search.html', {
        'title': f'{search_content} Results',
        'users': users,
        'tags': tags,
    })

# ! ---------------- MESSAGES ----------------
class MessageIndex(LoginRequiredMixin):
    def get(self, request):
        return render(request, 'messages/index.html')

class Room(LoginRequiredMixin, View):
    def get(self, request, room_name):
        room = MessageRoom.objects.filter(name=room_name).first()
        chats = []

        if room:
            messages = Message.objects.filter(room=room)
        else:
            room = MessageRoom(name=room_name)
            room.save()

        return render(request, 'messages/room.html', {'room_name': room_name, 'messages': messages})