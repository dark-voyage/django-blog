from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.helpers import generate_unique_slug, remove_tags
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        abstract = True


    @property
    def image_url(self):
        if hasattr(self, 'image'):
            return '%s%s' % (settings.HOST, self.image.url) if self.image else ''
        elif hasattr(self, 'icon'):
            return '%s%s' % (settings.HOST, self.icon.url) if self.icon else ''
        elif hasattr(self, 'thumbnail'):
            return '%s%s' % (settings.HOST, self.thumbnail.url) if self.thumbnail else ''
        return ''


    class Meta:
        abstract = True

class PostType(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        from blog.helpers import slug_check
        self.title = slug_check(Post, self)
        super(PostType, self).save()

    def __str__(self):
        return self.title


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    thumbnail = models.ImageField(upload_to='images/%Y/%m')
    body = RichTextUploadingField()
    views = models.IntegerField(default=0, editable=False)
    type = models.ForeignKey(PostType, on_delete=models.DO_NOTHING, null=True, blank=True)
    time = models.IntegerField(default=1, editable=False)

    def save(self, *args, **kwargs):
        import math
        self.time = math.ceil(len(remove_tags(self.body)) / 1400)
        from blog.helpers import slug_check
        self.title = slug_check(Post, self)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextUploadingField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    replied_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.replied_to is not None and self.post != self.replied_to.post:
            return ValidationError({"message":"You tried to access other one's account"})
        else:
            super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Comment in {self.post} and id {self.id}"


class Profile(BaseModel):
    image = models.ImageField(upload_to='images/%Y/%m', null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    try:
        Profile.objects.get(user=instance)
    except:
        Profile.objects.create(user=instance)






