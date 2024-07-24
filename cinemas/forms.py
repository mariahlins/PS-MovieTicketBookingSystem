from django import forms
from .models import Cinema, Room

class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['cinemaName', 'state', 'city', 'rooms']
        widgets = {
            'cinemaName': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields=['roomNumber','seats']
        labels={'roomNumber':'Room number', 'seats':'Number of seats'}
        