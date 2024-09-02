# forms.py
from django import forms
from .models import Movie
from users.models import Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'plot', 'duration', 'year','genre1','genre2', 'director', 'country', 'poster', 'rating', 'trailer_url']
        widgets = {
            'plot': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['comment','rate']

    def __init__(self, *args, **kwargs):
        self.movie = kwargs.pop('movie', None)
        self.profile = kwargs.pop('profile', None)
        super(ReviewForm, self).__init__(*args, **kwargs)  # Chama o __init__ da superclasse

    def clean(self):
        cleaned_data = super().clean()

        if not self.movie or not self.profile:
            raise forms.ValidationError("Erro interno: Filme ou perfil não fornecido.")

        self.instance.movie = self.movie
        self.instance.profile = self.profile

        if self.instance.pk is None:  
            if Review.objects.filter(movie=self.movie, profile=self.profile).exists():
                raise forms.ValidationError("Você já avaliou esse filme.")
            
        return cleaned_data
