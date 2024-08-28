from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Session, TicketCancelled
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.models import Profile, Wallet, CreditCard, DebitCard
from .forms import TicketForm
from django.db import IntegrityError
from django.contrib import messages

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

@login_required
def ticketHistory(request):
    try:
        tickets = Ticket.objects.filter(user=request.user.profile).order_by('-purchasedAt')
        ticketsc = TicketCancelled.objects.filter(user=request.user.profile).order_by('-cancelledAt')
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Ticket não encontrado")
    return render(request, 'tickets/ticketHistory.html', {'tickets': tickets, 'ticketsc':ticketsc})

@login_required
def activeTickets(request):
    try:
        active_tickets = Ticket.objects.filter(user=request.user.profile, status__in=['PENDING', 'DONE'])
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Ticket não encontrado")
    return render(request, 'tickets/activeTickets.html', {'active_tickets': active_tickets})

@login_required
def cancelledTicket(request):
    try:
        ticket_cancelled = TicketCancelled.objects.filter(user=request.user.profile)
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Ticket não encontrado")
    
    return render(request, 'tickets/cancelledTicket.html', {'ticket_cancelled': ticket_cancelled})

@login_required
def cancelTicket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Ticket não encontrado")
    
    if ticket.user == request.user.profile:
        try:
            ticket.cancel()
            messages.success(request, 'Ticket cancelado com sucesso!')
        except ValueError as e:
            messages.error(request, str(e))
    else:
        messages.error(request, 'Você não tem permissão para cancelar este ticket.')

    return redirect('ticketHistory')

#@login_required
#def payTicket(request, ticket_id):