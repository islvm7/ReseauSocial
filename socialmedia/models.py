from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
import uuid
from django.conf import settings


from django.contrib.auth.models import AbstractUser

#User = get_user_model()
class CustomUser(AbstractUser):
    interet=models.CharField(max_length=100, blank=True)
    location =  models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_pics', default='default.jpg')
    telephone = models.CharField(max_length=20, blank=True, default='')
    date_naissance = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.username
# Create your models here.
class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profileimg = models.ImageField(upload_to='profile_pics', default='default.jpg')
    
    def __str__(self):
        return self.user.username
    def get_interests_list(self):
        return [i.strip().lower() for i in self.location.split(',') if i.strip()]
    
    def __str__(self):
        return f"Profil de {self.user.username}"


class Post(models.Model):
    objects = None
    id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post de {self.author.username}"

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



class Friendship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
    ]
    
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='friendships_sent', 
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='friendships_received', 
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"

