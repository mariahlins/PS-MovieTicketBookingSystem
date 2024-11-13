from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movie
from .views import notifyNewMovie 

#vai conectar a função notifyNewMovie ao save de movie
#@receiver(post_save, sender=Movie)
#def notify_users_on_new_movie(sender, instance, created, **kwargs):
    #se for criado, aciona a função 
#    if created:
#        notifyNewMovie(instance)
