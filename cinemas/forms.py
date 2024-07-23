from django import forms
from .models import Cinema, Room

class CinemaForm(forms.ModelForm):
    class Meta:
        model=Cinema
        fields=['cinemaName','state','city','rooms']
        labels={'cinemaName':'Cinemas name', 'state':'State', 'city':'City', 'rooms':'Number of rooms'}

class RoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields=['roomNumber','seats']
        labels={'roomNumber':'Room number', 'seats':'Number of seats'}
        