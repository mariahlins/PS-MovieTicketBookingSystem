from django.db import models
from users.models import Profile
from sessoes.models import Session

class Ticket(models.Model):
    TICKET_TYPES=[
        ('MEIA', 'Meia Entrada'),
        ('IDOSO', 'Idoso'),
        ('NORMAL', 'Normal'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
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

            #descontos de tipos de entrada
            if ticketType == 'MEIA':
                self.price = self.session.price * 0.5
            elif ticketType == 'IDOSO':
                self.price = self.session.price * 0.6
            self.save()
        else:
            raise ValueError("Assento já reservado.")
