from django.urls import path
from . import views

urlpatterns=[
    path('tickets/<int:sessionId>', views.tickets, name='tickets'),
    path('ticket/<int:ticketId>', views.sessionTicket, name='sessionTicket'),
]