from django.shortcuts import render
from rest_framework.generics import \
    (ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView)
from blog.models import Post, Comment, Profile
from blog.serializers import PostSerializer, CommentSerializer, RegisterSerializer, ProfileSerializer
from blog.custom_permissions import AuthorAllStaffAllButEditOrReadOnly, OnlyAnonymous
from rest_framework import permissions
from django.contrib.auth.models import User


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post_slug = self.request.query_params.get('post_slug')
        return Comment.objects.filter(post__slug=post_slug)

class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentRUDView(RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AuthorAllStaffAllButEditOrReadOnly]

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permissions = [OnlyAnonymous,]

class ProfileRUDView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permissions = [AuthorAllStaffAllButEditOrReadOnly]



