from django.db import models
from users.models import Profile
from sessoes.models import Session
from decimal import Decimal

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
    
    def reserve(self, profile, ticketType):
        if not self.is_reserved:
            self.user = profile
            self.is_reserved = True
            self.ticketType = ticketType
            basePrice=self.price

            #descontos de tipos de entrada
            if ticketType == 'MEIA':
                self.price = round(basePrice * Decimal('0.5'), 2)
            elif ticketType == 'IDOSO':
                self.price = round(basePrice * Decimal('0.6'), 2)
            self.save()
        else:
            raise ValueError("Assento já reservado.")
        
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