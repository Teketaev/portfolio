from django.urls import path

from . import views

app_name = 'perms'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),

    path('post-create/', views.PostCreateView.as_view(), name='post_create'),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post-update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post-delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),

    path('post-detail/<int:pk>/add-comment/', views.PostDetailView.as_view(), name='comment_create'),
    path('comment-delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('ban-user/<int:user_id>/', views.BanUserView.as_view(), name='ban_user'),
    path('unban-user/<int:user_id>/', views.UnbanUserView.as_view(), name='unban_user'),
]