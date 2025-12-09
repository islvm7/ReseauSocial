from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profileimg = models.ImageField(upload_to='profile_pics', default='default.jpg')
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    objects = None
    id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user=models.CharField(max_length=100)

    def __str__(self):
        return self.user