from django.db import models
from movies.models import Movie
from cinemas.models import Room, Cinema

class Session(models.Model):

    HOURS = [
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('22:00', '22:00'),
        ('23:00', '23:00'),
    ]

    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema=models.ForeignKey(Cinema, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    date=models.DateField()
    hour=models.CharField(max_length=5, choices=HOURS)
    available_seats=models.PositiveIntegerField(default=0)
    price=models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        #aqui vai acessar o número de assentos disponiveis na sala
        if self.room:
            self.available_seats=self.room.seats
        super().save(*args, **kwargs)
