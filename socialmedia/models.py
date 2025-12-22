from django.db import models

import uuid
from datetime import datetime
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    bio = models.TextField(blank=True, verbose_name="Biographie")
    location = models.CharField(max_length=100, blank=True, verbose_name="Localisation")
    profileimg = models.ImageField(
        upload_to='profile_pics', 
        default='default.jpg',
        verbose_name="Photo de profil"
    )
    interet = models.TextField(
        blank=True, 
        help_text="Séparés par des virgules",
        verbose_name="Centres d'intérêt"
    )
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    date_naissance = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    
    def get_interests_list(self):
        """Retourne la liste des centres d'intérêt"""
        return [i.strip().lower() for i in self.interet.split(',') if i.strip()]
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅
        on_delete=models.CASCADE, 
        related_name='liked_posts'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

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


class PostView(models.Model):
    """Modèle pour tracker les vues de posts"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅
        on_delete=models.CASCADE, 
        related_name='viewed_posts'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.user.username} a vu {self.post.id}"


class PostComment(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

