# movies/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movie
from .views import notifyNewMovie  # Suponha que você tenha movido a função de e-mail para um arquivo utils.py

@receiver(post_save, sender=Movie)
def notify_users_on_new_movie(sender, instance, created, **kwargs):
    if created:
        notifyNewMovie(instance)
