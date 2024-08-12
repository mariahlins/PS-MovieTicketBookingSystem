from django.shortcuts import render, get_object_or_404
from .models import Ticket, Session
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .forms import TicketForm
from django.db import IntegrityError

def index(request):
    return render(request, 'cinemas/index.html')

@login_required
def tickets(request, sessionId):
    session = get_object_or_404(Session, id=sessionId)
    tickets = Ticket.objects.filter(session=session)
    context = {'session': session, 'tickets': tickets}
    return render(request, 'tickets/tickets.html', context)

@login_required
def sessionTicket(request, ticketId):
    try:
        ticket=Ticket.objects.get(id=ticketId)
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Ticket não encontrado")
    
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticketType = form.cleaned_data['ticketType']
            if not ticket.is_reserved:
                try:
                    ticket.reserve(profile, ticketType)
                    return HttpResponseRedirect(reverse('tickets', args=[ticket.session.id]))
                except IntegrityError:
                    form.add_error(None, "Erro ao reservar o ingresso. Verifique os dados e tente novamente.")
                except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        form = TicketForm(instance=ticket)
    context = {'ticket': ticket, 'form': form}
    return render(request, 'tickets/sessionTicket.html', context)