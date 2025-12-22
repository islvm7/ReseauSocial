from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .models import Profile, Post, LikePost, FollowersCount,Friendship, PostView
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.http import require_POST
from .post import ProfileUpdateForm,PostForm,SignUpForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .friend_recommendation import FriendRecommendation
from django.db.models import Q, Count
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model() 
from .content_recommendation import ContentRecommendation




@login_required(login_url="/login/")
def index (request):
   all_users = User.objects.exclude(username=request.user.username)  
   recommendations = FriendRecommendation.recommend_friends(request.user, limit=10)
   
    
   
   print(request.user.username)
   return render(request,'main/feed.html', {
        'username': request.user.username , 'recommendations': recommendations,
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
   user_profile = User.objects.filter(user=user_object).first()

   
   username_profile_list = []

   if request.method == "POST":
      username = request.POST.get('username', '').strip()  

      if username:  # Asigură-te că username-ul nu este gol
         # Găsește utilizatorii care se potrivesc cu termenul căutat
         username_object = User.objects.filter(username__icontains=username)

         # Găsește profilele asociate utilizatorilor
         for user in username_object:
            profile_lists = User.objects.filter(user=user)
            username_profile_list.append(profile_lists)

         # Combină toate profilele într-o singură listă
         username_profile_list = list(chain.from_iterable(username_profile_list))

   return render(request, 'search.html', {
      'user_profile': user_profile,
      'username_profile_list': username_profile_list
   })

def signup(request):
    """Vue d'inscription avec formulaire Django"""
    if request.user.is_authenticated:
        return redirect('socialmedia:index')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            # Créer l'utilisateur
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            
            # Connexion automatique après inscription
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username} ! Votre compte a été créé avec succès.')
                return redirect('home')
        else:
            # Afficher les erreurs
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = SignUpForm()
    
    context = {
        'form': form
    }
    return render(request, 'main/signup.html', context)


def signup_simple(request):
    """Vue d'inscription simple sans formulaire Django"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        # Validation
        errors = []
        
        if not username:
            errors.append("Le nom d'utilisateur est requis.")
        elif len(username) < 3:
            errors.append("Le nom d'utilisateur doit contenir au moins 3 caractères.")
        elif User.objects.filter(username=username).exists():
            errors.append("Ce nom d'utilisateur est déjà pris.")
        
        if not email:
            errors.append("L'email est requis.")
        elif User.objects.filter(email=email).exists():
            errors.append("Cet email est déjà utilisé.")
        
        if not password:
            errors.append("Le mot de passe est requis.")
        elif len(password) < 8:
            errors.append("Le mot de passe doit contenir au moins 8 caractères.")
        
        if password != password2:
            errors.append("Les mots de passe ne correspondent pas.")
        
        # Si des erreurs existent
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'main/signup.html', {
                'username': username,
                'email': email
            })
        
        # Créer l'utilisateur
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            
            # Connexion automatique
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username} ! Votre compte a été créé avec succès.')
                return redirect('home')
        
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du compte : {str(e)}")
            return render(request, 'main/signup.html')
    
    return render(request, 'main/signup.html')


@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    # L'utilisateur ne peut modifier que son propre profil
    user = request.user
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('socialmedia:index')
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'main/edit_profile.html', {'form': form, 'user': user})


@login_required(login_url="/login/")
def follow_user(request):
    follower = request.user.username
    user = request.POST.get("user")

    if FollowersCount.objects.filter(follower=follower, user=user).exists():
        FollowersCount.objects.filter(follower=follower, user=user).delete()
    else:
        FollowersCount.objects.create(follower=follower, user=user)

    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/login/")
def like_post(request, post_id):
    username = request.user.username
    post = Post.objects.get(id=post_id)

    like = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like:
        like.delete()
        post.no_of_likes -= 1
    else:
        LikePost.objects.create(post_id=post_id, username=username)
        post.no_of_likes += 1

    post.save()
    return redirect("socialmedia:feed")


@login_required(login_url="/login/")
def suggestions(request):
    user = request.user.username

    following = FollowersCount.objects.filter(follower=user).values_list('user', flat=True)

    all_users = User.objects.exclude(username=user)
    suggested_users = all_users.exclude(username__in=following)

    profiles = User.objects.filter(username__in=suggested_users)[:5]


    return render(request, "main/suggestions_partial.html", {"profiles": profiles})



@login_required(login_url="/login/")
def follow_user(request):
    follower = request.user.username
    user = request.POST.get("user")

    if FollowersCount.objects.filter(follower=follower, user=user).exists():
        FollowersCount.objects.filter(follower=follower, user=user).delete()
    else:
        FollowersCount.objects.create(follower=follower, user=user)

    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/login/")
def feed_view(request):
    """Vue principale du fil d'actualité avec recommandations"""
    
    # Recommandations personnalisées
    recommendations = ContentRecommendation.recommend_posts(request.user, limit=20)
    
    # Posts tendances (fallback si pas assez de recommandations)
    trending = ContentRecommendation.get_trending_posts(days=7, limit=10)
    
    context = {
        'recommendations': recommendations,
        'trending_posts': trending,
        'show_recommendations': len(recommendations) > 0
    }
    return render(request, 'main/feed.html', context)


@login_required(login_url="/login/")
@require_POST
def like_post(request, post_id):
    """Liker/unliker un post"""
    post = get_object_or_404(Post, id=post_id)
    
    like, created = LikePost.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # Unlike
        like.delete()
        post.no_of_likes = max(0, post.no_of_likes - 1)
        liked = False
    else:
        # Like
        post.no_of_likes += 1
        liked = True
    
    post.save()
    
    return JsonResponse({
        'liked': liked,
        'total_likes': post.no_of_likes
    })


@login_required(login_url="/login/")
def track_post_view(request, post_id):
    """Tracker la vue d'un post"""
    post = get_object_or_404(Post, id=post_id)
    
    # Créer ou mettre à jour la vue
    PostView.objects.get_or_create(user=request.user, post=post)
    
    return JsonResponse({'status': 'ok'})


@login_required
def discover_view(request):
    """Page de découverte avec posts tendances"""
    trending = ContentRecommendation.get_trending_posts(days=7, limit=30)
    
    context = {
        'trending_posts': trending
    }
    return render(request, 'main/discover.html', context)
