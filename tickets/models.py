from django.db import models
from users.models import Profile
from sessoes.models import Session
from decimal import Decimal
from django.utils import timezone

class Ticket(models.Model):
    TICKET_STATUS=[
        ('DONE', 'Concluído'),
        ('PENDING', 'Pendente'),
        ('CANCELLED', 'Cancelado'),
        ('FREE', 'Livre'),
    ]

    TICKET_TYPES=[
        ('MEIA', 'Meia Entrada'),
        ('IDOSO', 'Idoso'),
        ('NORMAL', 'Normal'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=TICKET_STATUS, default='FREE')
    seatNumber = models.PositiveIntegerField()
    ticketType = models.CharField(max_length=6, choices=TICKET_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_reserved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    purchasedAt = models.DateTimeField(auto_now_add=True)
    history = models.TextField(null=True, blank=True)
    
    def reserve(self, profile, ticketType):
        if not self.is_reserved:
            self.user = profile
            self.is_reserved = True
            self.ticketType = ticketType
            basePrice=self.price
            if self.status=='FREE':
                self.status = 'PENDING'

            #descontos de tipos de entrada
            if ticketType == 'MEIA':
                self.price = round(basePrice * Decimal('0.5'), 2)
            elif ticketType == 'IDOSO':
                self.price = round(basePrice * Decimal('0.6'), 2)
            self.save()
        else:
            raise ValueError("Assento já reservado.")
        
    def cancel(self):
        if self.is_reserved:
            TicketCancelled.objects.create(
                original_ticket_id=self.id,
                session=self.session,
                user=self.user,
                seatNumber=self.seatNumber,
                ticketType=self.ticketType,
                price=self.price,
                purchasedAt=self.purchasedAt,
                cancelledAt=timezone.now()
            )
            
            self.user = None
            self.status = 'FREE'
            self.is_reserved = False
            self.paid = False
            self.save()
        else:
            raise ValueError("O ticket não pode ser cancelado.")
        

class TicketCancelled(models.Model):
    original_ticket_id = models.PositiveIntegerField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    seatNumber = models.PositiveIntegerField()
    ticketType = models.CharField(max_length=6)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    purchasedAt = models.DateTimeField()
    cancelledAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Ticket Cancelado - ID Original: {self.original_ticket_id}"


class Payment(models.Model):

    PAYMENT_METHODS = [
        ('CREDIT_CARD', 'Cartão de Crédito'),
        ('DEBIT_CARD', 'Cartão de Débito'),
        ('PAYPAL', 'PayPal'),
        ('PIX', 'PIX'),
        ('BOLETO', 'Boleto Bancário'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('COMPLETED', 'Concluído'),
        ('FAILED', 'Falhado'),
        ('REFUNDED', 'Reembolsado'),
    ]

    ticket=models.ForeignKey(Ticket, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=6, decimal_places=2)
    payMethod=models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status=models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transactionId=models.CharField(max_length=100, unique=True)
    paidAt = models.DateTimeField(null=True, blank=True)
    createdAt=models.DateTimeField(auto_now_add=True)

    def process_payment(self):
        if self.status == 'PENDING':
            self.status = 'COMPLETED'
            self.paidAt = models.DateTimeField(auto_now=True)
            self.ticket.paid = True
            self.ticket.save()
            self.save()
        else:
            raise ValueError("Pagamento não pode ser processado. Status atual: " + self.status)

    def __str__(self):
        return f"Pagamento {self.status} - {self.ticket.user.user.email} - {self.amount} {self.currency}"