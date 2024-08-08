from django.urls import path
from . import views

urlpatterns=[
    path('tickets/<int:sessionId>', views.tickets, name='tickets'),
    path('sessionTicket/<int:ticketId>', views.sessionTicket, name='sessionTicket'),
]