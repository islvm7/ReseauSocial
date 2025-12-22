from django.db.models import Count, Q, F, ExpressionWrapper, FloatField
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from .models import Post

class ContentRecommendation:
    
    @staticmethod
    def extract_hashtags(text):
        """Extrait les hashtags d'un texte"""
        if not text:
            return []
        return re.findall(r'#(\w+)', text.lower())
    
    @staticmethod
    def extract_keywords(text):
        """Extrait des mots-clés d'un texte"""
        if not text:
            return []
        
        stopwords = {
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou',
            'est', 'sont', 'dans', 'pour', 'avec', 'sur', 'the', 'a', 'an',
            'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with'
        }
        
        words = re.findall(r'\b\w{3,}\b', text.lower())
        return [w for w in words if w not in stopwords]
    
    @staticmethod
    def get_user_interaction_score(user):
        """Calcule les scores d'interaction de l'utilisateur par auteur et par hashtag"""
        from .models import LikePost, PostComment, PostView
        
        # Score par auteur basé sur les likes
        likes = LikePost.objects.filter(user=user).select_related('post__user')
        author_scores = defaultdict(int)
        
        for like in likes:
            author_scores[like.post.user.id] += 3  # Like = 3 points
        
        # Score par auteur basé sur les commentaires
        comments = PostComment.objects.filter(user=user).select_related('post__user')
        for comment in comments:
            author_scores[comment.post.user.id] += 2  # Commentaire = 2 points
        
        # Extraction des hashtags des posts likés
        liked_posts = Post.objects.filter(likes__user=user)
        hashtag_scores = Counter()
        keyword_scores = Counter()
        
        for post in liked_posts:
            hashtags = ContentRecommendation.extract_hashtags(post.caption)
            keywords = ContentRecommendation.extract_keywords(post.caption)
            
            for tag in hashtags:
                hashtag_scores[tag] += 2
            
            for keyword in keywords:
                keyword_scores[keyword] += 1
        
        return {
            'authors': dict(author_scores),
            'hashtags': dict(hashtag_scores),
            'keywords': dict(keyword_scores)
        }
    
    @staticmethod
    def get_user_interests_from_profile(user):
        """Récupère les centres d'intérêt du profil utilisateur"""
        try:
            profile = user.profile
            return set(profile.get_interests_list())
        except:
            return set()
    
    @staticmethod
    def calculate_post_score(post, user, user_preferences, recency_weight=0.3):
        """Calcule le score de recommandation pour un post"""
        score = 0
        
        # 1. Score basé sur l'auteur (30%)
        author_scores = user_preferences.get('authors', {})
        if post.user.id in author_scores:
            author_score = min(author_scores[post.user.id] / 10, 1)  # Normalisation
            score += author_score * 0.3
        
        # 2. Score basé sur les hashtags (25%)
        post_hashtags = ContentRecommendation.extract_hashtags(post.caption)
        hashtag_scores = user_preferences.get('hashtags', {})
        
        if post_hashtags and hashtag_scores:
            matching_score = sum(hashtag_scores.get(tag, 0) for tag in post_hashtags)
            normalized_score = min(matching_score / 10, 1)
            score += normalized_score * 0.25
        
        # 3. Score basé sur les mots-clés (20%)
        post_keywords = ContentRecommendation.extract_keywords(post.caption)
        keyword_scores = user_preferences.get('keywords', {})
        
        if post_keywords and keyword_scores:
            matching_score = sum(keyword_scores.get(kw, 0) for kw in post_keywords)
            normalized_score = min(matching_score / 20, 1)
            score += normalized_score * 0.2
        
        # 4. Score basé sur les intérêts du profil (15%)
        user_interests = ContentRecommendation.get_user_interests_from_profile(user)
        if user_interests:
            caption_lower = post.caption.lower()
            matching_interests = sum(1 for interest in user_interests if interest in caption_lower)
            if matching_interests > 0:
                score += min(matching_interests / len(user_interests), 1) * 0.15
        
        # 5. Score de popularité (10%)
        popularity_score = min(post.no_of_likes / 100, 1)  # Normalisation
        score += popularity_score * 0.1
        
        # 6. Bonus de fraîcheur (recency_weight, par défaut 30%)
        hours_old = (datetime.now() - post.created_at.replace(tzinfo=None)).total_seconds() / 3600
        recency_score = max(0, 1 - (hours_old / 168))  # Décroissance sur 7 jours
        score += recency_score * recency_weight
        
        return score
    
    @staticmethod
    def recommend_posts(user, limit=20, exclude_own=True, min_score=0.1):
        """Recommande des posts pour un utilisateur"""
        from .models import LikePost, PostView
        
        # Posts déjà vus ou likés à exclure
        liked_post_ids = LikePost.objects.filter(user=user).values_list('post_id', flat=True)
        viewed_post_ids = PostView.objects.filter(
            user=user,
            viewed_at__gte=datetime.now() - timedelta(days=7)  # Vus dans les 7 derniers jours
        ).values_list('post_id', flat=True)
        
        excluded_ids = set(liked_post_ids) | set(viewed_post_ids)
        
        # Récupérer les préférences utilisateur
        user_preferences = ContentRecommendation.get_user_interaction_score(user)
        
        # Candidats potentiels
        posts_query = Post.objects.select_related('user').exclude(id__in=excluded_ids)
        
        if exclude_own:
            posts_query = posts_query.exclude(user=user)
        
        # Limiter aux posts récents (30 derniers jours) pour la performance
        posts_query = posts_query.filter(
            created_at__gte=datetime.now() - timedelta(days=30)
        )
        
        recommendations = []
        
        for post in posts_query:
            score = ContentRecommendation.calculate_post_score(
                post, user, user_preferences
            )
            
            if score >= min_score:
                recommendations.append({
                    'post': post,
                    'score': score,
                    'reason': ContentRecommendation.get_recommendation_reason(
                        post, user_preferences
                    )
                })
        
        # Tri par score décroissant
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:limit]
    
    @staticmethod
    def get_recommendation_reason(post, user_preferences):
        """Génère une explication de la recommandation"""
        reasons = []
        
        # Vérifier l'auteur
        if post.user.id in user_preferences.get('authors', {}):
            reasons.append(f"Vous aimez les posts de @{post.user.username}")
        
        # Vérifier les hashtags
        post_hashtags = ContentRecommendation.extract_hashtags(post.caption)
        matching_tags = [tag for tag in post_hashtags if tag in user_preferences.get('hashtags', {})]
        if matching_tags:
            reasons.append(f"Hashtags: #{', #'.join(matching_tags[:2])}")
        
        # Popularité
        if post.no_of_likes > 50:
            reasons.append(f"Post populaire ({post.no_of_likes} likes)")
        
        return " • ".join(reasons) if reasons else "Nouveau contenu"
    
    @staticmethod
    def get_trending_posts(days=7, limit=10):
        """Récupère les posts tendances"""
        since = datetime.now() - timedelta(days=days)
        
        trending = Post.objects.filter(
            created_at__gte=since
        ).annotate(
            engagement_score=ExpressionWrapper(
                F('no_of_likes') * 1.0 + Count('comments') * 2.0,
                output_field=FloatField()
            )
        ).order_by('-engagement_score', '-created_at')[:limit]
        
        return trending
