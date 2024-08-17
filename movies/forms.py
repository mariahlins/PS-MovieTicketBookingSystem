# forms.py
from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'plot', 'duration', 'year','genre1','genre2', 'director', 'country', 'poster', 'trailer_url','rating']
        widgets = {
            'plot': forms.Textarea(attrs={'rows': 4}),
        }

