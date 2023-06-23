import uuid
import boto3
import os
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
from main_app.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Post, Comment
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
    profile = request.user.profile
    followers = profile.following_list.all()
    posts_from_followed = Post.objects.filter(profile__in=followers)
    return render(request, 'qurate/feed.html', {
        'title': 'Your Feed',
        'posts': posts_from_followed
    })

def explore(request):
        posts = Post.objects.all()
        return render(request, 'qurate/explore.html', {
        'posts': posts,
        'title': 'Explore'
    })

# @ratelimit(key = ratelimitkey(user = 'user', rate = '10/s', method = ratelimit.ALL))
@ratelimit(key = 'ip', rate = '79/s', method = ratelimit.ALL)
def inspo(request):
    # pull data from 3rd party rest API
    # posts = Post.objects.all()
    response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=True&q=')
    # response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/objectIDs')
    # response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/49187')
    # convert reponse data into json
    explore_data = response.json()
    # ? change to explore_data['objectIDs'], pass that through, figure that out on front end
    posts = []
    idx = 0
    for post in explore_data['objectIDs']:
        print('Checkpoint ', idx)
        response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{post}')
        explore = response.json()
        posts.append(explore) 
        idx += 1
        if idx == 20:
            break
    # print(explore['objectIDs'])
    # print(posts)
    print('Checkpoint 2')
    # return HttpResponse("Explore")
    return render(request, 'qurate/inspiration.html', {
        'posts': posts,
        # 'explore': explore['objectIDs'],
        'title': 'Inspiration',
    })


def inspo(request):
    # pull data from 3rd party rest API
    # posts = Post.objects.all()
    response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=True&q=')
    # response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/objectIDs')
    # response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/49187')
    # convert reponse data into json
    inspo_data = response.json()
    # ? change to explore_data['objectIDs'], pass that through, figure that out on front end
    posts = []
    idx = 0
    for post in inspo_data['objectIDs']:
        print('Checkpoint ', idx)
        response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{post}')
        inspo = response.json()
        posts.append(inspo) 
        idx += 1
        if idx == 20:
            break
    # print(explore['objectIDs'])
    # print(posts)
    print('Checkpoint 2')
    # return HttpResponse("Explore")
    return render(request, 'qurate/inspiration.html', {
        'posts': posts,
        # 'inspiration': inspo['objectIDs'],
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
    success_url = '/posts'

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
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('user_feed')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
#! someone fix plz profile is always  1 behind user
def users_detail(request, user_id):
    profile = Profile.objects.get(id=user_id)
    # print(profile)
    user_posts = Post.objects.filter(user=user_id)
    # print(user_posts)
    profile1down = profile.user
    return render(request, 'users/detail.html', {
        #! fix this!!!
        'profile': profile,
        'title': f"{profile.user}'s Pofile",
        'posts': user_posts
    })

def follow(request, user_id):
    print('starting follow function')
    profile = Profile.objects.get(id=user_id)
    print(profile)
    user_posts = Post.objects.filter(user=user_id)
    print(user_posts)
    is_following = False

    if request.method == 'POST':
        if profile.follower_list.filter(id=request.user.id).exists():
            profile.follower_list.remove(request.user.profile)
            is_following = False
            print('follower removed')
        else:
            profile.follower_list.add(request.user.profile)
            is_following = True
            print('follower added')

    return render(request, 'users/detail.html', {
        'profile': profile,
        'title': f"{profile.user}'s Profile",
        'posts': user_posts,
        'is_following': is_following
    })

