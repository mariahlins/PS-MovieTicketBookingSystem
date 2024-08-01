from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from .forms import SignUpForm, SignUpFormStaff
from django.contrib.auth.decorators import login_required
from .models import Profile

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def perfilClient(request):
    return render(request, 'users/perfilClient.html')

@login_required
def perfilStaff(request):
    return render(request, 'users/perfilStaff.html')

@login_required
def perfilAdmin(request):
    users=Profile.objects.order_by('user')
    context={'users':users}
    return render(request, 'users/perfilAdmin.html', context)

def register(request):
    if request.method=='POST':
        form=SignUpForm(data=request.POST)
        if form.is_valid():
            newUser=form.save()
            """faz o login do usuario e redireciona para a pag inicial"""
            authenticatedUser=authenticate(username=newUser.username, password=request.POST['password'])
            login(request, authenticatedUser)
            return HttpResponseRedirect(reverse('index'))
    else:
        form=SignUpForm()

    context={'form':form}
    return render(request, 'users/register.html', context)

@login_required
def registerStaff(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        form = SignUpFormStaff(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SignUpFormStaff()

    context = {'form': form}
    return render(request, 'users/registerStaff.html', context)

"""@login_required
def editProfile(request, userId):
    profile=Profile.objects.get(id=userId)

    if request.method=='POST':
        form=SignUpForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('perfil'))
    else:
        form=SignUpForm(instance=profile)
    
    context={'profile':profile, 'form': form}
    return render(request, 'users/editProfile.html', context)

@login_required
def editStaff(request, userId):
    profile = Profile.objects.get(id=userId)
    
    #aqui vai copiar e apenas editar as informações sem editar a senha do funcionário
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data.pop('password', None)
        form = SignUpForm(post_data, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('perfilAdmin'))
    else:
        form = SignUpForm(instance=profile)

    context = {'profile': profile, 'form': form}
    return render(request, 'users/editStaff.html', context)"""
