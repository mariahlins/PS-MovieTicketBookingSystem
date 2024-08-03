from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cinemas/', views.cinemas, name='cinemas'),
    path('cinema/<int:cinemaId>/', views.cinema, name='cinema'),
    path('newCinema/', views.newCinema, name='newCinema'),
    path('editCinema/<int:cinemaId>', views.editCinema, name='editCinema'),
    path('newRoom/<int:cinemaId>', views.newRoom, name='newRoom'),
    path('editRoom/<int:roomId>', views.editRoom, name='editRoom'),
    path('deleteCinema/<int:cinemaId>', views.deleteCinema, name='deleteCinema'),
    path('deleteRoom/<int:roomId>', views.deleteRoom, name='deleteRoom'),
]