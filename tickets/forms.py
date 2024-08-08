from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['session','user','seatNumber', 'ticketType', 'price', 'is_reserved']
