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

]