from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from .models import Session
from .forms import FirstStepForm, SecondStepForm


@login_required
def sessions(request):
    sessions=Session.objects.order_by('date')
    context={'sessions':sessions}
    return render(request, 'sessoes/sessions.html', context)

@login_required
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

@login_required
def newSessionStep1(request):
    if request.method == 'POST':
        form = FirstStepForm(request.POST)
        if form.is_valid():
            request.session['movie_id'] = form.cleaned_data['movie'].id
            request.session['cinema_id'] = form.cleaned_data['cinema'].id
            return redirect('new_session_step2')
    else:
        form = FirstStepForm()
    return render(request, 'sessoes/newSessionStep1.html', {'form': form})

@login_required
def newSessionStep2(request):
    try:
        movie_id = request.session.get('movie_id')
        cinema_id = request.session.get('cinema_id')
    except Session.DoesNotExist:
        return HttpResponseNotFound("Filme ou cinema não encontrados")

    if not movie_id or not cinema_id:
        return redirect('new_session_step1')

    if request.method == 'POST':
        form = SecondStepForm(request.POST, cinema_id=cinema_id)
        if form.is_valid():
            session = form.save(commit=False)
            session.movie_id = movie_id
            session.cinema_id = cinema_id
            session.save()
            session.generateTickets()
            return redirect('sessions')
    else:
        form = SecondStepForm(cinema_id=cinema_id)
    
    return render(request, 'sessoes/newSessionStep2.html', {'form': form})

@login_required
def editSession(request, sessionId):
    try:
        session=Session.objects.get(id=sessionId)
    except Session.DoesNotExist:
        return HttpResponseNotFound("Sessão não encontrada")
    
    if request.method=='POST' and 'step1' in request.POST:
        form=FirstStepForm(request.POST)
        if form.is_valid():
            session.movie_id=form.cleaned_data['movie'].id
            session.cinema_id=form.cleaned_data['cinema'].id
            session.save()
            request.session['movie_id']=session.movie_id
            request.session['cinema_id']=session.cinema_id
            return redirect('edit_session_step2', sessionId=sessionId)
    else:
        initial_data = {
            'movie':session.movie,
            'cinema':session.cinema,
        }
        form=FirstStepForm(initial=initial_data)

    context={'form':form, 'session':session}
    return render(request, 'sessoes/editSession.html', context)

@login_required
def editSessionStep2(request, sessionId):
    try:
        session=Session.objects.get(id=sessionId)
    except Session.DoesNotExist:
        return HttpResponseNotFound("Sessão não encontrada")
    
    cinema_id = request.session.get('cinema_id', session.cinema.id)

    if request.method=='POST' and 'step2' in request.POST:
        form=SecondStepForm(request.POST, cinema_id=cinema_id)
        if form.is_valid():
            session.room = form.cleaned_data['room']
            session.date = form.cleaned_data['date']
            session.hour = form.cleaned_data['hour']
            session.save()
            return redirect('sessions')
    else:
        initial_data={
            'room':session.room,
            'date':session.date,
            'hour':session.hour,
        }
        form=SecondStepForm(initial=initial_data, cinema_id=cinema_id)
    
    context={'form':form, 'session':session}
    return render(request, 'sessoes/editSession2.html', context)
