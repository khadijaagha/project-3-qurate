import uuid
import boto3
import os
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
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
    return render(request, 'qurate/feed.html', {
        'title': 'Your Feed'
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
    inspo_data = response.json()
    # ? change to inspo_data['objectIDs'], pass that through, figure that out on front end
    # posts = []
    # idx = 0
    # for post in inspo_data['objectIDs']:
    #     print('Checkpoint ', idx)
    #     response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{post}')
    #     inspo = response.json()
    #     posts.append(inspo) 
    #     idx += 1
    #     if idx == 20:
    #         break
    # print(inspo['objectIDs'])
    # print(posts)
    print('Checkpoint 2')
    # return HttpResponse("Inspiration")
    return render(request, 'qurate/inspiration.html', {
        # 'posts': posts,
        'inspo': inspo_data['objectIDs'],
        'title': 'Inspiration',
    })


# def inspo(request):
#     # pull data from 3rd party rest API
#     # posts = Post.objects.all()
#     response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=True&q=')
#     # response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/objectIDs')
#     # response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/49187')
#     # convert reponse data into json
#     inspo_data = response.json()
#     # ? change to explore_data['objectIDs'], pass that through, figure that out on front end
#     posts = []
#     idx = 0
#     for post in inspo_data['objectIDs']:
#         print('Checkpoint ', idx)
#         response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{post}')
#         inspo = response.json()
#         posts.append(inspo) 
#         idx += 1
#         if idx == 20:
#             break
#     # print(explore['objectIDs'])
#     # print(posts)
#     print('Checkpoint 2')
#     # return HttpResponse("Explore")
#     return render(request, 'qurate/inspiration.html', {
#         'posts': posts,
#         # 'inspiration': inspo['objectIDs'],
#         'title': 'Inspiration',
#     })

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
    profile = Profile.objects.get(id=user_id - 1)
    user_posts = Post.objects.filter(user=user_id)
    profile1down = profile.user
    return render(request, 'users/detail.html', {
        #! fix this!!!
        'title': f"{profile.user}'s Pofile",
        'posts': user_posts
    })