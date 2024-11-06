from django.shortcuts import render, get_object_or_404, redirect
from abc import ABC, abstractmethod
import qrcode.constants
from decimal import Decimal
from django.utils import timezone
from .models import Ticket, Session, TicketCancelled, Payment, Coupon
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.models import Profile, CreditCard, DebitCard
from .forms import TicketForm, CouponForm
from django.db import IntegrityError
from django.core.exceptions import ValidationError
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


#########################

#implementação do template method para reserva de ticket

class TicketReservationTemplate(ABC):
    def __init__(self, request, ticket, profile):
        self.request = request
        self.ticket = ticket
        self.profile = profile
        self.form = TicketForm(request.POST or None, instance=self.ticket)

    def process(self):
        #esse método vai definir o fluxo da reserva do ticket
        if self.ticket.is_reserved:
            return self.redirect_with_message('tickets', 'Ticket já reservado', self.ticket.session.id)
        
        if self.request.method=='POST' and self.form.is_valid():
            try:
                self.apply_coupon()
                self.reserve_ticket()
                messages.success(self.request, "Ticket reservado com sucesso!")
                return self.redirect('tickets', self.ticket.session.id)
            except Exception as e:
                self.handle_exception(e)
        
        return render(self.request, 'tickets/sessionTickets,html', {'ticket':self.ticket, 'form':self.form})
    
    @abstractmethod
    def apply_coupon(self):
        pass

    @abstractmethod
    def reserve_ticket(self):
        pass

    def handle_exception(self, exception):
        if isinstance(exception, ValidationError):
            self.form.add_error(None, str(exception))
        elif isinstance(exception, IntegrityError):
            self.form.add_error(None, "Erro ao reservar o ingresso. Verifique os dados e tente novamente.")
        else:
            self.form.add_error(None, f"Erro inesperado: {exception}")
    
    def redirect_with_message(self, view_name, message, *args):
        messages.error(self.request, message)
        return HttpResponseRedirect(reverse(view_name, args=args))
    
    def redirect(self, view_name, *args):
        return HttpResponseRedirect(reverse(view_name, args=args))

class DefaultTicketReservation(TicketReservationTemplate):
    def apply_coupon(self):
        coupon_code = self.request.POST.get('coupon_code')
        if not coupon_code:
            raise ValidationError("Nenhum código de cupom foi fornecido.")
        
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
        except Coupon.DoesNotExist:
            raise ValidationError("O cupom não foi encontrado ou está expirado.")
        
        #verifica se está inválido ou expirado
        if not coupon.is_valid() or coupon.validUntil > timezone.now :
            raise ValidationError("O cupom está expirado ou inválido.")
        
        discount_amount=(self.price * coupon.discount) / Decimal('100.0')
        self.price=round(self.price - discount_amount, 2)
        self.coupon=coupon
        self.save()


    def reserve_ticket(self):
        ticket_type = self.request.POST.get('ticket_type')

        if ticket_type not in dict(Ticket.TICKET_TYPES):
            raise ValidationError("Tipo de ticket inválido. Tente novamente.")
        
        self.ticket.user = self.profile
        self.ticket.is_reserved = True
        self.ticket.ticketType = ticket_type
        self.ticket.staty = 'PENDING'

        base_price = self.ticket.price
        if ticket_type == 'MEIA':
            self.price = round(base_price * Decimal('0.5'), 2)
        elif ticket_type == 'IDOSO':
            self.price = round(base_price * Decimal('0.6'), 2)

        self.ticket.save()
        

@login_required
def sessionTicket(request, ticketId):
    try:
        ticket=Ticket.objects.get(id=ticketId)
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Ticket não encontrado")
    
    profile = get_object_or_404(Profile, user=request.user)

    reservation = DefaultTicketReservation(request, ticket, profile)
    return reservation.process()


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