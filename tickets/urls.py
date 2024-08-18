from django.urls import path
from . import views

urlpatterns=[
    path('tickets/<int:sessionId>', views.tickets, name='tickets'),
    path('ticket/<int:ticketId>', views.sessionTicket, name='sessionTicket'),
    path('activeTickets/',views.activeTickets, name='activeTickets'),
    path('ticketHistory/',views.ticketHistory, name='ticketHistory'),
    path('cancelledTicket/',views.cancelledTicket, name='cancelledTicket'),
    path('cancelTicket/<int:ticket_id>/', views.cancelTicket, name='cancelTicket'),
]