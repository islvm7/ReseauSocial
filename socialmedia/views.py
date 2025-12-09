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
from django.contrib.auth.models import User, auth
from django.views.decorators.http import require_POST
from .post import PostForm
from .post import ProfileUpdateForm
from .models import Profile
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


@login_required(login_url="/login/")
def index (request):
   print(request.user.username)
   return render(request,'main/feed.html', {
        'username': request.user.username
    })
@login_required(login_url="/login/")
@require_POST
def logout_user(request):
    logout(request)
    url=reverse_lazy('socialmedia:login')
    return redirect(url)


@login_required(login_url="/login/")
def upload(request):
   if request.method == "POST":
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user.username
        post.save()
        return redirect('socialmedia:post')  
   else:
          form = PostForm()

    
   return render(request, 'main/post.html', {'form': form})
   
@login_required(login_url="/login/")
def search(request):
   
   user_object = User.objects.get(username=request.user.username)
   user_profile = Profile.objects.filter(user=user_object).first()

   
   username_profile_list = []

   if request.method == "POST":
      username = request.POST.get('username', '').strip()  

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

def signup(request):
   if request.method=="POST": #procesarea datelor din form
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      password2 = request.POST['password2']

      if password == password2:
         if User.objects.filter(email=email).exists():
            messages.info(request,'Email taken')
            return redirect('socialmedia:signup')
            # se face redirect catre path-ul din urls.py
         elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('socialmedia:signup')
         else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()

             #lLog user in and redirect to settings
            user_login = auth.authenticate(username=username,password=password)
            auth.login(request, user_login)

             #create a profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('socialmedia:index')
      else:
         messages.info(request,'Password not matching')
         return redirect('socialmedia:signup')

   else:
      #return redirect('signup')
      return render(request,'main/signup.html')


@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    user_id = request.GET.get('user_id')
    
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user
    
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('socialmedia:index')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'main/edit_profile.html', {'form': form})