from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Session
from .forms import SessionForm

@login_required
def sessions(request):
    sessions=Session.objects.order_by('date')
    context={'sessions':sessions}
    return render(request, 'sessoes/sessions.html', context)

@staff_member_required
def newSession(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sessions')
    else:
        form = SessionForm()
    return render(request, 'sessoes/newSession.html', {'form': form})
