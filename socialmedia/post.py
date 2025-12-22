from django import forms
from .models import Post,CustomUser
from django.contrib.auth import get_user_model

User = get_user_model() 
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    """Formulaire d'inscription personnalisé"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom (optionnel)'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom (optionnel)'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmez le mot de passe'
        })
    
    def clean_email(self):
        """Vérifie que l'email n'existe pas déjà"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email
    
    def clean_username(self):
        """Vérifie que le username n'existe pas déjà"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

class ProfileUpdateForm(forms.ModelForm):
    """Formulaire pour mettre à jour le profil utilisateur"""
    class Meta:
        model = CustomUser
        fields = ['profileimg', 'bio', 'location', 'interet', 'telephone', 'date_naissance']
        widgets = {
            'profileimg': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Parlez-nous de vous...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre ville'
            }),
            'interet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'python, django, football...'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+213...'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
class UserUpdateForm(forms.ModelForm):
    """Formulaire pour mettre à jour les infos de base"""
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
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