from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post, LikePost, PostComment, Friendship

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Configuration de l'admin pour CustomUser"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'location', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'location']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Ajouter les champs personnalisés dans l'admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informations personnelles', {
            'fields': ('bio', 'location', 'profileimg', 'interet', 'telephone', 'date_naissance')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations personnelles', {
            'fields': ('bio', 'location', 'profileimg', 'interet', 'telephone', 'date_naissance')
        }),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'caption_preview', 'no_of_likes', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'caption']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Légende'

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__caption']

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'text_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'text']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Commentaire'

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['from_user__username', 'to_user__username']
