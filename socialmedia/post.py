from django import forms
from .models import Post,Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profileimg', 'location']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
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