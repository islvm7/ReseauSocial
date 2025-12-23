from django.urls import path, include
from . import views

app_name = 'socialmedia'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),
    path('logout/', views.logout_user, name='logout'),
]