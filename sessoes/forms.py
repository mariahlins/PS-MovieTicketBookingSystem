from django import forms
from .models import Session
from movies.models import Movie
from cinemas.models import Cinema, Room

class FirstStepForm(forms.Form):
    movie = forms.ModelChoiceField(queryset=Movie.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    cinema = forms.ModelChoiceField(queryset=Cinema.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

class SecondStepForm(forms.ModelForm):
    date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    hour = forms.ChoiceField(choices=Session.HOURS, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Session
        fields = ['room', 'date', 'hour', 'price']
        
    def __init__(self, *args, **kwargs):
        cinema_id = kwargs.pop('cinema_id', None)
        super().__init__(*args, **kwargs)
        if cinema_id:
            self.fields['room'].queryset = Room.objects.filter(cinema_id=cinema_id)
