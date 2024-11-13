from .observer import Observer
from io import BytesIO
from users.models import Profile
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import qrcode

class TicketEmailNotificationObserver(Observer):
    def update(self, event_type, data):
        if event_type == 'reservation':
            self.sendTicketEmail(data['user'], data['ticket'], data['payment'])

    def sendTicketEmail(self, user, ticket, payment):
        qr_data = f"Ticket ID:{ticket.id}, Sessão: {ticket.session.movie.title}, Hora: {ticket.session.hour}, Assento: {ticket.seatNumber}"
        
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10, border=4
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
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

class NewMovieNotificationObserver(Observer):
    def update(self, event_type, data):
        if event_type == 'new_movie':
            self.notifyNewMovie(data['movie'])

    def notifyNewMovie(self, movie):
        # Busca todos os usuários com notificações de filmes ativadas
        users = Profile.objects.filter(receive_movie_notifications=True)

        for user in users:
            context = {'user': user, 'movie': movie}
            html_content = render_to_string('movies/newMovieNotify.html', context)
            text_content = strip_tags(html_content)

            email = EmailMessage(
                subject=f"Novo filme disponível: {movie.title}",
                body=text_content,
                from_email='cinepass.p3@gmail.com',
                to=[user.user.email]
            )
            email.content_subtype = 'html'
            email.send()