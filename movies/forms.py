# forms.py
from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'plot', 'duration', 'year', 'director', 'country', 'poster', 'rating']
        widgets = {
            'plot': forms.Textarea(attrs={'rows': 4}),
        }

