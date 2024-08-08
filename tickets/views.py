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
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticketType = form.cleaned_data['ticketType']
            if not ticket.is_reserved:
                # Obtenha o perfil do usuário autenticado
                profile = Profile.objects.get(user=request.user)
                ticket.reserve(profile, ticketType)
                return HttpResponseRedirect(reverse('tickets', args=[ticket.session.id]))
    else:
        form = TicketForm(instance=ticket)
    context = {'ticket': ticket, 'form': form}
    return render(request, 'tickets/sessionTicket.html', context)

def change(request, ticketId):
    ticket = get_object_or_404(Ticket, id=ticketId)
    ticket.is_reserved = True
    ticket.save()
    return HttpResponseRedirect(reverse('tickets', args=[ticket.session.id]))

@login_required
def confirmPayment(request, ticketId):
    ticket=get_object_or_404(Ticket, id=ticketId)
    if request.method=='POST':
        ticket.confirmPayment()
        return HttpResponseRedirect(reverse('tickets', args=[ticket.session.id]))
    context={'ticket': ticket}
    return render(request, 'tickets/confirmPayment.html', context)
