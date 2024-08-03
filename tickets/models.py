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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    purchased_at = models.DateTimeField(auto_now_add=True)
    ticket_type = models.CharField(max_length=6, choices=TICKET_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.price:
            if self.ticket_type == 'MEIA':
                #meia entrada
                self.price = self.session.price * 0.5 
            elif self.ticket_type == 'IDOSO':
                #desconto de 40% para idoso
                self.price = self.session.price * 0.6
            else:
                self.price = self.session.price
        super().save(*args, **kwargs)
