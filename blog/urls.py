from django.urls import path
from blog import views
urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('comments/<str:post_slug>/', views.CommentListView.as_view(), name='comment_list'),
    path('comment/create/', views.CommentCreateView.as_view(), name='comment_create'),

    path('comment/<int:pk>/', views.CommentRUDView.as_view(), name='comment_edit'),
    path('profile/<int:pk>/', views.ProfileRUDView.as_view(), name='profile_edit'),
]