from django import forms
from django.forms import ModelForm, Textarea
from .models import Post


class NewPost(forms.Form):
    text = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)