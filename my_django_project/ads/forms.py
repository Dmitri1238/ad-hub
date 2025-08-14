from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'city']

class RequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()