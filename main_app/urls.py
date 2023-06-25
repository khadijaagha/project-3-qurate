from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #! --- DIFFERENT FEEDS/EXPLORE/INSPO
    path('qurate/', views.user_feed, name='user_feed'),
    path('explore/', views.explore, name='explore'),
    path('qurate/inspiration/', views.inspo, name='inspo'),
    #!----POST ROUTES-----
    # * path('posts/<int:post_id>/', views.posts_detail, name='detail'),
    path('posts/<int:pk>/', views.posts_detail, name='detail'),
    path('posts/create/', views.PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    #! --------- SEARCH URL
    path('qurate/search/', views.search, name='search'),
    #!----COMMENT ROUTES-----
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    # * path('posts/<int:pk>/comment/<int:fk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
    path('posts/<int:post_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('posts/<int:post_id>/comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    #!------------ USER ROUTES 
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/', views.users_detail, name='profile'),
    path('profile/<int:user_id>/follow/', views.follow, name='follow'),
    #! -------------- TAG ROUTES
    path('qurate/<str:tags>/', views.tags_index, name='tags')
    #! -------------- MESSAGE ROUTES --------------
    # ? idk if this routing is correct
    # ? path('messages/', views.MessageIndex.as_view(), name='messages')
]
