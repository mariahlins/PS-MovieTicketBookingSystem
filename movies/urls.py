from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies, name='movies'), 
    path('movie/<int:movieId>', views.movie, name='movie'), 
    path('newmovie', views.newmovie, name='newmovie'), 
    path('deleteMovie/<int:movieId>', views.deleteMovie, name='deleteMovie'), 
    path('editMovie/<int:movieId>', views.editMovie, name='editMovie'), 
    path('newReview/<int:ticketId>', views.newReview, name='newReview'), 
    path('editReview/<int:reviewId>', views.editReview, name='editReview'), 
    path('deleteReview/<int:reviewId>', views.deleteReview, name='deleteReview'), 
]