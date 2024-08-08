from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model=Ticket
        fields=['ticketType']
        labels={'ticketType':'Tipo de ingresso'}
        widgets={'ticketType': forms.Select(choices=Ticket.TICKET_TYPES)}