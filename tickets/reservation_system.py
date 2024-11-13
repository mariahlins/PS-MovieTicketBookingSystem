from observer import Subject
from observer.notifications import TicketEmailNotificationObserver
from django.db import transaction
from tickets.models import Ticket
from .views import DefaultTicketReservation

class ReservationSystem(Subject):
    def __init__(self):
        super().__init__()
        self.add_observer(TicketEmailNotificationObserver())

    def create_reservation(self, request, ticket_id, profile):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            reservation = DefaultTicketReservation(request, ticket, profile)

            # Processa a reserva dentro de uma transação
            with transaction.atomic():
                response = reservation.process()

                # Notifica observadores se a reserva foi bem-sucedida (ticket foi reservado)
                if ticket.is_reserved:
                    reservation_data = {
                        'user': profile.user,
                        'ticket': ticket,
                        'payment': None 
                    }
                    self.notify_observers('reservation', reservation_data)

                return response

        except Ticket.DoesNotExist:
            return {
                'status': 'error',
                'message': 'Ticket não encontrado'
            }
