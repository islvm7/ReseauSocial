from django.db.models import Q, Count
from collections import defaultdict
import math
import re
from .models import Friendship
from django.contrib.auth import get_user_model

User = get_user_model() 


class FriendRecommendation:
    
    @staticmethod
    def get_friends(user):
        
        friends_ids = Friendship.objects.filter(
            Q(from_user=user, status='accepted') | 
            Q(to_user=user, status='accepted')
        ).values_list('from_user_id', 'to_user_id')
        
        friend_ids = set()
        for from_id, to_id in friends_ids:
            friend_ids.add(from_id if from_id != user.id else to_id)
        
        return User.objects.filter(id__in=friend_ids)
    
    @staticmethod
    def extract_keywords_from_bio(bio):
        """Extrait des mots-clés pertinents de la bio"""
        if not bio:
            return set()
        
        # Mots vides à ignorer
        stopwords = {
            'le', 'la', 'les', 'un', 'une', 'des', 'je', 'tu', 'il', 'elle',
            'nous', 'vous', 'ils', 'elles', 'de', 'du', 'et', 'ou', 'mais',
            'donc', 'or', 'ni', 'car', 'the', 'a', 'an', 'and', 'or', 'but',
            'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'am', 'are',
            'suis', 'es', 'est', 'sommes', 'êtes', 'sont', 'mon', 'ma', 'mes',
            'ton', 'ta', 'tes', 'son', 'sa', 'ses', 'ce', 'cette', 'ces'
        }
        
        # Extraction des mots (3+ caractères)
        words = re.findall(r'\b\w{3,}\b', bio.lower())
        return set(w for w in words if w not in stopwords)
    
    @staticmethod
    def get_interests_list(user):
        """Convertit la chaîne d'intérêts en liste"""
        if not user.interet:
            return []
        # Sépare par virgule, point-virgule ou slash
        interests = re.split(r'[,;/]', user.interet)
        return [interest.strip().lower() for interest in interests if interest.strip()]
    
    @staticmethod
    def jaccard_similarity(set1, set2):
        """Calcule la similarité de Jaccard entre deux ensembles"""
        if not set1 or not set2:
            return 0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0
    
    @staticmethod
    def profile_similarity(user1, user2):
        """Calcule la similarité entre deux profils utilisateurs"""
        score = 0
        
        # 1. Similarité des centres d'intérêt explicites (poids: 0.4)
        interests1 = set(FriendRecommendation.get_interests_list(user1))
        interests2 = set(FriendRecommendation.get_interests_list(user2))
        if interests1 and interests2:
            interests_score = FriendRecommendation.jaccard_similarity(interests1, interests2)
            score += interests_score * 0.4
        
        # 2. Similarité des bios (poids: 0.3)
        bio_keywords1 = FriendRecommendation.extract_keywords_from_bio(user1.bio)
        bio_keywords2 = FriendRecommendation.extract_keywords_from_bio(user2.bio)
        if bio_keywords1 and bio_keywords2:
            bio_score = FriendRecommendation.jaccard_similarity(bio_keywords1, bio_keywords2)
            score += bio_score * 0.3
        
        # 3. Même localisation (poids: 0.3)
        if user1.location and user2.location:
            if user1.location.strip().lower() == user2.location.strip().lower():
                score += 0.3
        
        return score
    
    @staticmethod
    def friends_of_friends_score(user, candidate):
        """Calcule le score basé sur les amis communs"""
        user_friends = set(FriendRecommendation.get_friends(user).values_list('id', flat=True))
        candidate_friends = set(FriendRecommendation.get_friends(candidate).values_list('id', flat=True))
        
        common_friends = user_friends.intersection(candidate_friends)
        return len(common_friends)
    
    @staticmethod
    def recommend_friends(user, limit=10):
        """Recommande des amis pour un utilisateur"""
        # Obtenir les amis actuels et les demandes en attente
        current_friends = FriendRecommendation.get_friends(user)
        current_friends_ids = set(current_friends.values_list('id', flat=True))
        
        pending_ids = Friendship.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status='pending'
        ).values_list('from_user_id', 'to_user_id')
        
        excluded_ids = current_friends_ids.copy()
        excluded_ids.add(user.id)
        for from_id, to_id in pending_ids:
            excluded_ids.add(from_id)
            excluded_ids.add(to_id)
        
        # Candidats potentiels
        candidates = User.objects.exclude(id__in=excluded_ids)
        
        recommendations = []
        
        for candidate in candidates:
            # Calcul des scores
            profile_score = FriendRecommendation.profile_similarity(user, candidate)
            mutual_friends = FriendRecommendation.friends_of_friends_score(user, candidate)
            
            # Score final (60% similarité profil + 40% amis communs)
            # Normalisation du score des amis communs
            mutual_friends_normalized = min(mutual_friends / 10, 1)
            final_score = (profile_score * 0.6) + (mutual_friends_normalized * 0.4)
            
            if final_score > 0:  # Seulement si score positif
                recommendations.append({
                    'user': candidate,
                    'score': final_score,
                    'mutual_friends': mutual_friends,
                    'profile_score': profile_score
                })
        
        # Tri par score décroissant
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:limit]
    
    @staticmethod
    def get_mutual_friends(user1, user2):
        """Obtient la liste des amis communs entre deux utilisateurs"""
        user1_friends = set(FriendRecommendation.get_friends(user1).values_list('id', flat=True))
        user2_friends = set(FriendRecommendation.get_friends(user2).values_list('id', flat=True))
        
        common_friends_ids = user1_friends.intersection(user2_friends)
        return User.objects.filter(id__in=common_friends_ids)


