from django.contrib import admin
from blog.models import Profile, Post, PostType, Comment, Profile

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostType)
admin.site.register(Comment)

