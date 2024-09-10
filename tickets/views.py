from django.shortcuts import render, get_object_or_404, redirect
import qrcode.constants
from .models import Ticket, Session, TicketCancelled, Payment, Coupon
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.models import Profile, CreditCard, DebitCard
from .forms import TicketForm, CouponForm
from django.db import IntegrityError
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode

def index(request):
    return render(request, 'cinemas/index.html')

def tickets(request, sessionId):
    try:
        session=Session.objects.get(id=sessionId)
    except Session.DoesNotExist:
        return HttpResponseNotFound("Sessão não encontrada")
    
    tickets=Ticket.objects.filter(session=session)
    context={'session': session, 'tickets': tickets}
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
            coupon_code=form.cleaned_data['coupon_code']
            ticketType = form.cleaned_data['ticketType']
            if not ticket.is_reserved:
                try:
                    if coupon_code:
                        try:
                            coupon=Coupon.objects.get(code=coupon_code, active=True)
                            if coupon.is_valid():
                                discount_amount=ticket.price*(coupon.discount/100)
                                ticket.price-=discount_amount
                                ticket.coupon=coupon
                            else:
                                form.add_error('coupon_code',"Cupom invalido ou expirado")
                        except Coupon.DoesNotExist:
                            form.add_error('coupon_code',"Cupom não encontrado")

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

@login_required
def payTicket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Ticket não encontrado")
    
    if ticket.paid:
        messages.error(request,"O pagamento já foi efetuado.")
        return HttpResponseRedirect(reverse('ticketHistory'))
    
    profile = request.user.profile
    wallet = profile.wallet

    if request.method=='POST':
        payment_method=request.POST.get('payment_method')

        if payment_method=='WALLET':
            if wallet.balance>=ticket.price:
                wallet.deduct_balance(ticket.price)
                payment=Payment.objects.create(
                    ticket=ticket,
                    amount=ticket.price,
                    payMethod='WALLET',
                    status='COMPLETED',
                    transactionId=get_random_string(20)
                )

                ticket.paid=True
                ticket.status='DONE'
                ticket.save()
                sendTicketEmail(request.user,ticket,payment)
                messages.success(request, "Pagamento concluído com sucesso.")
                return HttpResponseRedirect(reverse('ticketHistory'))
            else:
                messages.error(request,"Saldo insuficiente.")

        elif payment_method=='CREDIT_CARD':
            card_id=request.POST.get('card_id')
            try:
                card=CreditCard.objects.get(id=card_id)
            except CreditCard.DoesNotExist:
                return HttpResponseNotFound("Cartão não encontrado.")
            
            payment=Payment.objects.create(
                ticket=ticket,
                amount=ticket.price,
                payMethod='CREDIT_CARD',
                status='COMPLETED',
                transactionId=get_random_string(20)
            )
            ticket.paid=True
            ticket.status='DONE'
            ticket.save()
            sendTicketEmail(request.user,ticket,payment)
            messages.success(request,"Pagamento concluído com sucesso usando cartão de crédito.")
            return HttpResponseRedirect(reverse('ticketHistory'))

        elif payment_method=='DEBIT_CARD':
            card_id=request.POST.get('card_id')
            try:
                card=DebitCard.objects.get(id=card_id)
            except CreditCard.DoesNotExist:
                return HttpResponseNotFound("Cartão não encontrado.")
            
            payment=Payment.objects.create(
                ticket=ticket,
                amount=ticket.price,
                payMethod='CREDIT_CARD',
                status='COMPLETED',
                transactionId=get_random_string(20)
            )
            ticket.paid=True
            ticket.status='DONE'
            ticket.save()
            sendTicketEmail(request.user,ticket,payment)
            messages.success(request,"Pagamento concluído com sucesso usando cartão de debito.")
            return HttpResponseRedirect(reverse('ticketHistory'))

        elif payment_method=='PIX':     
            payment=Payment.objects.create(
                ticket=ticket,
                amount=ticket.price,
                payMethod='PIX',
                status='COMPLETED',
                transactionId=get_random_string(20)
            )
            ticket.paid=True
            ticket.status='DONE'
            ticket.save()
            sendTicketEmail(request.user,ticket,payment)
            messages.success(request,"Pagamento concluído com sucesso usando pix.")
            return HttpResponseRedirect(reverse('ticketHistory'))
        
        else:
            messages.error(request,"Metódo de pagamento inválido ou falha no pagamento.")

    context={'ticket':ticket,'wallet_balance':wallet.balance,'credit_cards':wallet.credit_cards.all(), 'debit_cards':wallet.debit_cards.all()}
    return render(request, 'tickets/payTicket.html', context)

@login_required
def coupons(request):
    coupons=Coupon.objects.order_by('validUntil')
    return render(request,'tickets/coupons.html', {'coupons':coupons})

@login_required
def newCoupon(request):
    if request.method!='POST':
        form=CouponForm()
    else:
        form=CouponForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect(reverse('coupons'))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violaçãpo de integridade.")
            except Exception as e:
                form.add_error(None, f"Erro inesperado: {e}")

    return render(request, 'tickets/newCoupon.html', {'form':form})

def editCoupon(request, coupon_id):
    try:
        coupon=Coupon.objects.get(id=coupon_id)
    except Coupon.DoesNotExist:
        return HttpResponseNotFound("Cupom não encontrado.")
    
    if request.method=='POST':
        form=CouponForm(instance=coupon, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect(reverse('coupons'))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        form=CouponForm(instance=coupon)
    
    return render(request, 'tickets/editCoupon.html', {'coupon':coupon, 'form':form})

def sendTicketEmail(user, ticket, payment):
    qrData=f"Ticket ID:{ticket.id}, Sessão: {ticket.session.movie.title}, Hora: {ticket.session.hour},Assento: {ticket.seatNumber}"
    qr=qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10, border=4
    )

    qr.add_data(qrData)
    qr.make(fit=True)

    img=qr.make_image(fill='black', back_color='white')
    buffer=BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qrCodeImage=ContentFile(buffer.read(), name=f'ticket_{ticket.id}_qrcode.png')

    context={'user':user,'ticket':ticket,'payment':payment}
    htmlContent=render_to_string('tickets/ticketConfirmation.html', context)
    textContent=strip_tags(htmlContent)

    email=EmailMessage(
        subject=f"Confirmação de Pagamento e Ticket - {ticket.session.movie.title}",
        body=textContent,
        from_email='cinepass.p3@gmail.com',
        to=[user.email],
    )
    email.attach(qrCodeImage.name, qrCodeImage.read(), 'image/png')
    email.content_subtype='html'
    email.send()