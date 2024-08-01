from django.db import models
from movies.models import Movie
from cinemas.models import Room
from users.models import Profile

"""class Ticket(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    room_name = models.CharField(max_length=100)
    room_number = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.room:
            self.room_name = self.room.name
            self.room_number = self.room.number
        super().save(*args, **kwargs)"""
