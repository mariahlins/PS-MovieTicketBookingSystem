from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies, name='movies'), 
    path('movie/<int:movieId>', views.movie, name='movie'), 
    path('newmovie', views.newmovie, name='newmovie'), 
]