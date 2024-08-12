from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from .models import Session
from .forms import SessionForm
from django.db import IntegrityError

@login_required
def sessions(request):
    sessions=Session.objects.order_by('date')
    context={'sessions':sessions}
    return render(request, 'sessoes/sessions.html', context)

@login_required
def newSession(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            try:
                newSession=form.save()
                newSession.generateTickets()
                return redirect('sessions')
            except IntegrityError:
                form.add_error(None,"Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        form = SessionForm()
    return render(request, 'sessoes/newSession.html', {'form': form})

def deleteSession(request, sessionId):
    try:
        session=Session.objects.get(id=sessionId)
    except Session.DoesNotExist:
        return HttpResponseNotFound("Sessão não encontrada")

    if request.method == 'POST':
        session.delete()
        return HttpResponseRedirect(reverse('sessions'))

    context = {'session': session}
    return render(request, 'sessoes/deleteSession.html', context)