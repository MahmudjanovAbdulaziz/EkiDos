from django import forms
from .models import *



class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'inp'}),
        max_length=500
    )
    class Meta:
        model = Comments
        fields = ['text']



class AddProfileForm(forms.ModelForm):
    class Meta:
        model = AddProfile
        fields = ['first_name', 'last_name', 'img']