import uuid
import boto3
import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
from main_app.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Post, Comment
from .forms import UserCreationForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# @login_required
def user_feed(request):

    return render(request, 'qurate/feed.html', {

    })

def explore(request):
        return render(request, 'qurate/explore.html', {

    })

def inspo(request):
        return render(request, 'qurate/inspiration.html', {

    })

# @login_required
def posts_detail(request, posts_id):

    return render(request, 'posts/detail.html', {

    })

class PostCreate(CreateView):
    model = Post
    fields = ['url', 'title', 'price', 'description', 'tags']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'price', 'description', 'tags']

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/posts'


def add_comment(request, post_id):
 return render(request, 'posts/add_comment.html', {

    })


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment



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
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def users_detail(request, user_id):
    profile = Profile.objects.get(id=user_id)
    user_form = UserCreationForm()
    return render(request, 'users/detail.html', {
        'profile': profile, 'user_form': user_form,
    })


def explore_index(request):
    posts = Post.objects.all()
    return render(request, 'qurate/explore.html', {
        'posts': posts
    })