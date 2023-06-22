import uuid
import boto3
import os
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

class add_post(CreateView):
    pass
    model = Post
    fields = '__all__'

# @login_required
def posts_index(request):
    # posts = Post.objects.filter(user=request.user)
    return render(request, 'posts/index.html', {
        # 'posts': posts
    })

# @login_required
def posts_detail(request, posts_id):
    # post = Post.objects.get(id=post_id)
    # First, create a list of the toy ids that the cat DOES have
    # id_list = cat.toys.all().values_list('id')
    # # Query for the toys that the cat doesn't have
    # # by using the exclude() method vs. the filter() method
    # toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    # # instantiate FeedingForm to be rendered in detail.html
    # feeding_form = FeedingForm()
    return render(request, 'posts/detail.html', {
        # 'post': post, 'feeding_form': feeding_form,
        # 'toys': toys_cat_doesnt_have
    })

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = '__all__'
    
    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'price', 'description', 'tags']

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/posts'

# @login_required
def add_comment(request, post_id):
    # create a ModelForm instance using 
    # the data that was submitted in the form
    # form = CommentForm(request.POST)
    # # validate the form
    # if form.is_valid():
    #     # We want a model instance, but
    #     # we can't save to the db yet
    #     # because we have not assigned the
    #     #! similarly, for post_id FK cat_id FK. 
    #     new_comment = form.save(commit=False)
    #     new_comment.post_id = post_id
    #     new_comment.save()
    # return redirect('detail', post_id_id=post_id)
 return render(request, 'posts/add_comment.html', {
        # 'post': post, 'feeding_form': feeding_form,
        # 'toys': toys_cat_doesnt_have
    })


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment


# class ToyList(LoginRequiredMixin, ListView):
#     model = Toy

# class ToyDetail(LoginRequiredMixin, DetailView):
#     model = Toy

# class ToyCreate(LoginRequiredMixin, CreateView):
#     model = Toy
#     fields = '__all__'

# class ToyUpdate(LoginRequiredMixin, UpdateView):
#     model = Toy
#     fields = ['name', 'color']

# class ToyDelete(LoginRequiredMixin, DeleteView):
#     model = Toy
#     success_url = '/toys'

# @login_required
# def assoc_toy(request, cat_id, toy_id):
#     Cat.objects.get(id=cat_id).toys.add(toy_id)
#     return redirect('detail', cat_id=cat_id)

# @login_required
# def unassoc_toy(request, cat_id, toy_id):
#     Cat.objects.get(id=cat_id).toys.remove(toy_id)
#     return redirect('detail', cat_id=cat_id)

# @login_required
# def add_photo(request, cat_id):
#     # photo-file will be the "name" attribute on the <input type="file">
#     photo_file = request.FILES.get('photo-file', None)
#     if photo_file:
#         s3 = boto3.client('s3')
#         # need a unique "key" for S3 / needs image file extension too
#         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#         # just in case something goes wrong
#         try:
#             bucket = os.environ['S3_BUCKET']
#             s3.upload_fileobj(photo_file, bucket, key)
#             # build the full url string
#             url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
#             # we can assign to cat_id or cat (if you have a cat object)
#             Photo.objects.create(url=url, cat_id=cat_id)
#         except Exception as e:
#             print('An error occurred uploading file to S3')
#             print(e)
#     return redirect('detail', cat_id=cat_id)


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
    # First, create a list of the toy ids that the cat DOES have
    # id_list = cat.toys.all().values_list('id')
    # Query for the toys that the cat doesn't have
    # by using the exclude() method vs. the filter() method
    # toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    # instantiate FeedingForm to be rendered in detail.html
    user_form = UserCreationForm()
    return render(request, 'users/detail.html', {
        'profile': profile, 'user_form': user_form,
    })


def explore_index(request):
    posts = Post.objects.all()
    return render(request, 'qurate/explore.html', {
        'posts': posts
    })