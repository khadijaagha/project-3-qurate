from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('about/', views.about, name='about'),
    #!----POST ROUTES-----
    path('posts/', views.posts_index, name='index'),
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),
    path('posts/create/', views.PostCreate.as_view(), name='posts_create'),
    # path('posts/create/', views.PostCreate, name='posts_create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
    #!----COMMENT ROUTES-----
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/comment/<int:fk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
    # path('posts/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('posts/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    # path('posts/<int:cat_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    # path('toys/', views.ToyList.as_view(), name='toys_index'),
    # path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    # path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    # path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    # path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/', views.users_detail, name='profile'),
    #! ------------------ post paths
    path('qurate/add_post/', views.add_post.as_view(), name='add_post'),
]


#hello