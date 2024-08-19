from django import forms
from .models import Session
from movies.models import Movie
from cinemas.models import Cinema, Room
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, time


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

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        date = cleaned_data.get('date')
        hour = cleaned_data.get('hour')

        if date and hour:
            # Verificar se a data e hora são no futuro
            now = timezone.now()
            session_datetime = timezone.make_aware(datetime.combine(date, time(int(hour.split(':')[0]), int(hour.split(':')[1]))))
            if session_datetime <= now:
                raise ValidationError("A data e hora da sessão devem ser no futuro.")

            # Verificar se já existe uma sessão com a mesma sala, data e hora
            if room and Session.objects.filter(room=room, date=date, hour=hour).exists():
                raise ValidationError("Já existe uma sessão para esta sala, data e horário.")

        return cleaned_data


class FirstStepForm(forms.Form):
    movie = forms.ModelChoiceField(queryset=Movie.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    cinema = forms.ModelChoiceField(queryset=Cinema.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
