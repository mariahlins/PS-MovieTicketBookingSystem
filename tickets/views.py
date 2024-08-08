from django.shortcuts import render, get_object_or_404
from .models import Ticket, Session

def tickets(request, sessionId):
    session=get_object_or_404(Session, id=sessionId)
    tickets=Ticket.objects.filter(session=session)
    context={'session': session, 'tickets': tickets}
    return render(request, 'tickets/tickets.html', context)