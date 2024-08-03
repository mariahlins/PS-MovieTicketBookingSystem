from django import forms
from .models import Session

class SessionForm(forms.ModelForm):
    date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = Session
        fields = ['movie', 'cinema', 'room', 'date', 'hour', 'price']
        