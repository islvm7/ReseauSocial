from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Friendship

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administration du modèle CustomUser"""
    # Ajoutez vos champs personnalisés dans l'admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('telephone', 'bio', 'date_naissance', 'avatar')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('telephone', 'bio', 'date_naissance')
        }),
    )

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    """Administration des amitiés"""
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')
    readonly_fields = ('created_at', )
