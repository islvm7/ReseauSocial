from django import forms
from .models import Post
from django.contrib.auth import get_user_model
User = get_user_model()  

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'telephone', 
            'date_naissance',
            'location', 
            'interet', 
            'bio', 
            'profileimg'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+213 XXX XXX XXX'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville, Pays'
            }),
            'interet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sport, Musique, Voyage...'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Parlez-nous de vous...'
            }),
            'profileimg': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email',
            'location': 'Localisation',
            'interet': "Centres d'intérêt",
            'bio': 'Biographie',
            'profileimg': 'Photo de profil'
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image', 'user']

        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'post-textarea',
                'placeholder': 'Quoi de neuf ?'
            }),
            'user': forms.HiddenInput(),
        }