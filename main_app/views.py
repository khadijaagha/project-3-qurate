import uuid
import boto3
import os
import requests
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import UserCreationForm
from django_ratelimit.decorators import ratelimit

# ! ---------------- LIKES FUNCTION ----------------
def get_likes(posts, profile):
    for post in posts:
        likes = Profile.objects.filter(post_likes=post).count()
        post.likes = likes
        post.save()
        if profile.post_likes.filter(id=post.id).exists():
            post.user_liked = True
            post.save()
        elif not profile.post_likes.filter(id=post.id).exists():
            post.user_liked = False
            post.save()

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
    profile = Profile.objects.get(user=request.user.id)
    
    get_likes(user_posts, profile)

    return render(request, 'qurate/feed.html', {
        'title': 'Your Feed',
        'posts': user_posts
    })

def explore(request):
        posts = Post.objects.all().order_by('created_at')
        profile = Profile.objects.get(user=request.user.id)

        get_likes(posts, profile)

        return render(request, 'qurate/explore.html', {
            'posts': posts,
            'title': 'Explore'
        })

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


def posts_detail(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post).order_by('likes').reverse()
    profile = Profile.objects.get(user=request.user.id)
    likes = Profile.objects.filter(post_likes=post).count()
    post.likes = likes
    post.save()
    if profile.post_likes.filter(id=post.id).exists():
        post.user_liked = True
        post.save()
    elif not profile.post_likes.filter(id=post.id).exists():
        post.user_liked = False
        post.save()
    if request.method == 'POST':
        comment_body = request.POST.get('comment-body')
        comment = Comment.objects.create(body=comment_body, user=request.user, post=post)

    for comment in comments:
        likes = Profile.objects.filter(comment_likes=comment).count()
        comment.likes = likes
        comment.save()
        if profile.comment_likes.filter(id=comment.id).exists():
            comment.user_liked = True
            comment.save()
        elif not profile.comment_likes.filter(id=comment.id).exists():
            comment.user_liked = False
            comment.save()

    return render(request, 'posts/detail.html', {
        'post': post,
        'comments': comments,
        'title': 'Post Details',   
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
    success_url = reverse_lazy('user_feed')


def delete_post(request, post_id):
    
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.delete()
        print("Post deleted 🗑️")
        posts = Post.objects.all().order_by('created_at')        

    return render(request, 'qurate/explore.html', {
        'posts': posts,
        'title': 'Explore'
    })



@login_required
def like_post(request, pk):
    post = Post.objects.get(id=pk)
    profile = Profile.objects.get(user=request.user.id)

    if not profile.post_likes.filter(id=pk).exists():
        profile.post_likes.add(post)
        profile.save()
        print("Like button clicked 👍", pk)
    elif profile.post_likes.filter(id=pk).exists():
        profile.post_likes.remove(post)
        profile.save()
        print("Like removed 👎", pk)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# ! COMMENTS ---------------------

def add_comment(request, post_id):
    return render(request, 'posts/add_comment.html', {

    })

@login_required
def like_comment(request, post_id, comment_id):

    comment = Comment.objects.get(id=comment_id)
    profile = Profile.objects.get(user=request.user.id)

    if not profile.comment_likes.filter(id=comment_id).exists():
        profile.comment_likes.add(comment)
        profile.save()
        print("Comment like button clicked 👍", comment_id)
    elif profile.comment_likes.filter(id=comment_id).exists():
        profile.comment_likes.remove(comment)
        profile.save()
        print("Comment like removed 👎", comment_id)

    return redirect('detail', post_id)

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment

@login_required
def delete_comment(request, comment_id, post_id ):

    if request.method == 'POST':
        comment = Comment.objects.get(user=request.user, id=comment_id)
        comment.delete()
    return redirect('detail', post_id)


# ! TAGS ----------------------
def tags_index(request, tags):
    posts = Post.objects.filter(tags=tags)
    profile = Profile.objects.get(user=request.user.id)

    get_likes(posts, profile)
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
            following_users = request.user.profile.follows.all()
            user_posts = Post.objects.filter(user__profile__in=following_users).order_by('created_at')
            return redirect('user_feed')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def users_detail(request, user_id):
    profile = Profile.objects.get(id=user_id)
    viewer_profile = Profile.objects.get(id=request.user.id)
    user_posts = Post.objects.filter(user=user_id)
    post_count = Post.objects.filter(user=user_id).count();
    if profile.followed_by.filter(id=request.user.id).exists():
        is_following = True;
    else:
        is_following = False;
    get_likes(user_posts, viewer_profile)

    return render(request, 'users/detail.html', {
        'profile': profile,
        'title': f"{profile.user}'s Profile",
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


# ! ----------------  SEARCH ---------------- 

def search(request):
    search_content = request.POST.get('search')
    tags = []
    users = []
    if search_content[0] == '#':
        no_hash = search_content.strip('#')
        tags = Post.objects.filter(tags__icontains=no_hash)
        profile = Profile.objects.get(user=request.user.id)
        get_likes(tags, profile)
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
def MessageIndex(request):
    all_rooms = MessageRoom.objects.filter(participants=request.user)
    print(all_rooms)
    return render(request, 'messages/index.html', {
        'title': 'Your messages',
        'all_rooms': all_rooms
    })

def send_message(request, receiver_id):
    if request.method == 'POST':
        print('if')
        print(receiver_id)
        body = request.POST.get('body')
        receiver = User.objects.get(id=receiver_id)
        print(f'receiver {receiver}')
        sender = request.user
        print(f'sender {sender}')
        room = MessageRoom.objects.filter(participants=sender).filter(participants=receiver).first()
        if room is None:
            room_name = f"{sender.username} - {receiver.username}"
            room = MessageRoom.objects.create(name=room_name)
            room.participants.add(sender, receiver)
        message = Message.objects.create(body=body, sender=sender, room=room)
        return redirect('message_room', room_id=room.id)
    else:
        print('else')
        receiver = User.objects.get(pk=receiver_id)
        return render(request, 'messages/room.html', {
            'receiver': receiver
        })

def message_room(request, room_id):
    room = MessageRoom.objects.get(id=room_id)
    messages = room.messages.all().order_by('timestamp')
    receiver = room.participants.exclude(id=request.user.id).first()
    
    return render(request, 'messages/room.html', {
        'room': room,
        'messages': messages,
        'receiver': receiver,
        'title': room
    })