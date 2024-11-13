from abc import ABC, abstractmethod
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode

class Observer(ABC):
    @abstractmethod
    def update(self, ticket, event_type):
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, ticket, event_type):
        for observer in self._observers:
            observer.update(ticket, event_type)

class TicketEmailObserver(Observer):
    def update(self, ticket, event_type):
        if event_type == 'payment_completed':
            self.send_ticket_email(ticket)

    def send_ticket_email(self, ticket):
        user = ticket.user.user
        payment = ticket.payment_set.last()

        qr_data = f"Ticket ID: {ticket.id}, Sessão: {ticket.session.movie.title}, Hora: {ticket.session.hour}, Assento: {ticket.seatNumber}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        qr_code_image = ContentFile(buffer.read(), name=f'ticket_{ticket.id}_qrcode.png')

        context = {'user': user, 'ticket': ticket, 'payment': payment}
        html_content = render_to_string('tickets/ticketConfirmation.html', context)
        text_content = strip_tags(html_content)

        email = EmailMessage(
            subject=f"Confirmação de Pagamento e Ticket - {ticket.session.movie.title}",
            body=text_content,
            from_email='cinepass.p3@gmail.com',
            to=[user.email],
        )
        email.attach(qr_code_image.name, qr_code_image.read(), 'image/png')
        email.content_subtype = 'html'
        email.send()
