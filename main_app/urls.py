from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('about/', views.about, name='about'),
    #! --- DIFFERENT FEEDS/EXPLORE/INSPO
    path('qurate/', views.user_feed, name='user_feed'),
    path('qurate/explore/', views.explore, name='explore'),
    path('qurate/inspiration/', views.inspo, name='inspo'),
    #!----POST ROUTES-----
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),
    path('posts/create/', views.PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    #!----COMMENT ROUTES-----
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/comment/<int:fk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/', views.users_detail, name='profile'),
    #! -------------- TAG ROUTES
    path('qurate/<str:tags>/', views.tags_index, name='tags')
]
