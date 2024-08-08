from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Session
from .forms import SessionForm

@login_required
def sessions(request):
    sessions=Session.objects.order_by('date')
    context={'sessions':sessions}
    return render(request, 'sessoes/sessions.html', context)

def newSession(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            newSession=form.save()
            newSession.generateTickets()
            return redirect('sessions')
    else:
        form = SessionForm()
    return render(request, 'sessoes/newSession.html', {'form': form})

def deleteSession(request, sessionId):
    session = get_object_or_404(Session, id=sessionId)

    if request.method == 'POST':
        session.delete()
        return HttpResponseRedirect(reverse('sessions'))

    context = {'session': session}
    return render(request, 'sessoes/deleteSession.html', context)