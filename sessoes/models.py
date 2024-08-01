from django.db import models
from movies.models import Movie
from cinemas.models import Room
from users.models import Profile

class Session(models.Model):

    HOURS=[
        ('13H00','13'),
        ('14H00','14'),

        ('16H00','16'),
        ('17H00','17'),

        ('19H00','19'),
        ('20H00','20'),
        
        ('22H00','22'),
        ('23H00','23'),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    hour = models.IntegerField(choices=HOURS)

    def save(self, *args, **kwargs):
        if self.room:
            self.room_name = self.room.name
            self.room_number = self.room.number
        super().save(*args, **kwargs)
