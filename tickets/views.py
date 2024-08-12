from django.shortcuts import render, get_object_or_404
from .models import Ticket, Session
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .forms import TicketForm

def index(request):
    return render(request, 'cinemas/index.html')

@login_required
def tickets(request, sessionId):
    session = get_object_or_404(Session, id=sessionId)
    tickets = Ticket.objects.filter(session=session)
    context = {'session': session, 'tickets': tickets}
    return render(request, 'tickets/tickets.html', context)

def sessionTicket(request, ticketId):
    ticket = get_object_or_404(Ticket, id=ticketId)
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticketType = form.cleaned_data['ticketType']
            if not ticket.is_reserved:
                ticket.reserve(profile, ticketType)
                return HttpResponseRedirect(reverse('tickets', args=[ticket.session.id]))
    else:
        form = TicketForm(instance=ticket)
    context = {'ticket': ticket, 'form': form}
    return render(request, 'tickets/sessionTicket.html', context)