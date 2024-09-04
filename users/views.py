from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignUpFormStaff
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Wallet, CreditCard, DebitCard
from tickets.models import Payment
from django.db import IntegrityError
from decimal import Decimal
import uuid

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

@login_required
def user(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    
    users=Profile.objects.order_by('user')
    context={'users':users}
    return render(request, 'users/user.html', context)

def register(request):
    if request.method=='POST':
        form=SignUpForm(data=request.POST)
        if form.is_valid():
            try:
                newUser=form.save()
                authenticatedUser=authenticate(username=newUser.username, password=request.POST['password'])
                login(request, authenticatedUser)
                return HttpResponseRedirect(reverse('index'))
            except IntegrityError:
                form.add_error(None, "Erro ao criar o usuário. Dados duplicados ou violação de integridade.")
            except Exception as e:
                form.add_error(form.add_error(None, f"Erro inesperado: {e}"))
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
            try:
                form.save()
                return HttpResponseRedirect(reverse('index'))
            except IntegrityError:
                form.add_error(None, "Erro ao criar o funcionário. Dados duplicados ou violação de integridade")
            except Exception as e:
                form.add_error(None, f"Erro inesperado: {e}")
    else:
        form = SignUpFormStaff()

    context = {'form': form}
    return render(request, 'users/registerStaff.html', context)

@login_required
def editProfile(request):
    profile = request.user

    if request.method == 'POST':
        post_data = request.POST.copy()
        form = SignUpForm(post_data, instance=profile)

        if form.is_valid():
            try:
                form.save(commit=False)
                birth_date = form.cleaned_data.get('birth_date')
                profile.birth_date = birth_date
                profile.save()
                return HttpResponseRedirect(reverse('perfilClient'))
            except IntegrityError:
                form.add_error(None, "Erro ao editar perfil. Dados duplicados ou violação de integridade.")
            except Exception as e:
                form.add_error(None, f"Erro inesperado: {e}")
    else:
        #tendo certeza de que as informações serão preenchidas
        form = SignUpForm(instance=profile)

    context = {'profile': profile, 'form': form}
    return render(request, 'users/editProfile.html', context)


@login_required
def editStaff(request, userId):
    try:
        profile = Profile.objects.get(id=userId)
    except Profile.DoesNotExist:
        return HttpResponseNotFound("Usuário não encontrado")
    user = profile.user 

    if request.method == 'POST':
        post_data = request.POST.copy()

        if 'password' not in post_data or not post_data['password']:
            post_data.pop('password', None)
        
        form = SignUpFormStaff(post_data, instance=user)

        if form.is_valid():
            form.save(commit=False)
            
            birth_date = form.cleaned_data.get('birth_date')
            profile.birth_date = birth_date
            profile.save()

            user.is_staff = form.cleaned_data.get('is_staff')
            user.is_superuser = form.cleaned_data.get('is_superuser')
            user.save()
            
            return HttpResponseRedirect(reverse('perfilAdmin'))
    else:
        try:
            #tendo certeza de que as informações serão preenchidas
            initial_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'birth_date': profile.birth_date,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
            form = SignUpFormStaff(instance=user, initial=initial_data)
        except Exception as e:
            form = SignUpFormStaff()
            form.add_error(None, f"Erro ao carregar os dados do usuário: {e}")

    context = {'profile': profile, 'form': form}
    return render(request, 'users/editStaff.html', context)


#wallet
@login_required
def recharge(request):
    if request.method=='POST':
        amount=Decimal(request.POST.get('amount'))

        if amount>0:
            #verifica se a carteira existe, se não existir, cria uma nova para o usuário
            wallet, created= Wallet.objects.get_or_create(profile=request.user.profile)
            
            #uuid serve para gerar um id único para a transação
            transaction_id=str(uuid.uuid4())

            payment=Payment.objects.create(
                ticket=None, #é none pq é uma recarga e não de fato uma compra
                amount=amount,
                payMethod='PIX',
                status='COMPLETED',
                transactionId=transaction_id
            )

            wallet.add_balance(amount)
            messages.success(request, f"A quantia de R$ {amount} foi adicionada com sucesso à sua carteira via PIX!")
            return redirect('walletDetail')
        else:
            messages.error(request, "Valor inválido.")
    
    return render(request, 'users/recharge.html')

@login_required
def walletDetail(request):
    try:
        wallet=Wallet.objects.get(profile=request.user.profile)
    except Wallet.DoesNotExist:
        return HttpResponseNotFound("Carteira não encontrada. Tente novamente.")
    credit_cards = wallet.credit_cards.all()
    debit_cards = wallet.debit_cards.all()
    
    return render(request, 'users/walletDetail.html', {'wallet':wallet,'credit_cards': credit_cards,'debit_cards': debit_cards})

@login_required
def addCreditCard(request):
    if request.method=='POST':
        card_holder=request.POST.get('card_holder')
        card_number=request.POST.get('card_number')
        expiration_date=request.POST.get('expiration_date')
        cvv=request.POST.get('cvv')

        wallet, created=Wallet.objects.get_or_create(profile=request.user.profile)
        CreditCard.objects.create(
            wallet=wallet,
            card_holder=card_holder,
            card_number=card_number,
            expiration_date=expiration_date,
            cvv=cvv
        )
        return redirect('walletDetail')
    
    return render(request, 'users/addCreditCard.html')

@login_required
def addDebitCard(request):
    if request.method=='POST':
        card_holder=request.POST.get('card_holder')
        card_number=request.POST.get('card_number')
        expiration_date=request.POST.get('expiration_date')
        cvv=request.POST.get('cvv')

        wallet, created=Wallet.objects.get_or_create(profile=request.user.profile)
        DebitCard.objects.create(
            wallet=wallet,
            card_holder=card_holder,
            card_number=card_number,
            expiration_date=expiration_date,
            cvv=cvv
        )
        return redirect('walletDetail')
    
    return render(request, 'users/addDebitCard.html')