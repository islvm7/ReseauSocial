from django.urls import path,include
from . import views

app_name = 'socialmedia'
urlpatterns = [
    
    path('', include('django.contrib.auth.urls')),
    path('', views.index,name='index'),
    path('post/',views.upload,name='post'),
    path('signup/',views.signup,name='signup'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path("suggestions/", views.suggestions, name="suggestions"),
    path("search/", views.search, name="search"),
    path("follow/", views.follow_user, name="follow_user"),
    path("like/<str:post_id>/", views.like_post, name="like_post"),
    path('feed/', views.feed_view, name='feed'),
    path('discover/', views.discover_view, name='discover'),
    path('post/<uuid:post_id>/like/', views.like_post, name='like_post'),
    path('post/<uuid:post_id>/view/', views.track_post_view, name='track_post_view'),
    

]