from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method=='POST':
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            newUser=form.save()
            """faz o login do usuario e redireciona para a pag inicial"""
            authenticatedUser=authenticate(username=newUser.username, password=request.POST['password1'])
            login(request, authenticatedUser)
            return HttpResponseRedirect(reverse('index'))
    else:
        form=UserCreationForm()

    context={'form':form}
    return render(request, 'users/register.html', context)
    