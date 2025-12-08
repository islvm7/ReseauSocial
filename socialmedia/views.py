from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

@login_required(login_url="/login/")
def index (request):
   return render(request,'base.html')
@login_required(login_url="/login/")
def logout_user(request):
    logout(request)
    url=reverse_lazy('socialmedia:login')
    return redirect(url)


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "dashboard.html")

@login_required(login_url="/login/")
def upload(request):
   if request.method == 'POST':
      user = request.user.username
      image = request.FILES.get('image_upload')
      caption = request.POST['caption']

      new_post = Post.objects.create(user=user,image=image,caption=caption)
      new_post.save()

      return redirect('/')
   else:
      return redirect('/')
   
@login_required(login_url="/login/")
def search(request):
   # Obține obiectele utilizatorului conectat
   user_object = User.objects.get(username=request.user.username)
   user_profile = Profile.objects.filter(user=user_object).first()

   # Inițializează lista profilelor pentru rezultate
   username_profile_list = []

   if request.method == "POST":
      username = request.POST.get('username', '').strip()  # Obține username-ul căutat

      if username:  # Asigură-te că username-ul nu este gol
         # Găsește utilizatorii care se potrivesc cu termenul căutat
         username_object = User.objects.filter(username__icontains=username)

         # Găsește profilele asociate utilizatorilor
         for user in username_object:
            profile_lists = Profile.objects.filter(user=user)
            username_profile_list.append(profile_lists)

         # Combină toate profilele într-o singură listă
         username_profile_list = list(chain.from_iterable(username_profile_list))

   return render(request, 'search.html', {
      'user_profile': user_profile,
      'username_profile_list': username_profile_list
   })


