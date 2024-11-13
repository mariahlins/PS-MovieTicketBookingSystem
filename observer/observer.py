from tickets.views import sendTicketEmail
from movies.views import notifyNewMovie

class Observer:
    def update(self, event_type, data):
        raise NotImplementedError("Subclasses must implement this method")

class ReservationNotificationObserver(Observer):
    def update(self, event_type, data):
        if event_type == 'reservation':
            user = data['user']
            ticket = data['ticket']
            payment = data['payment']
            sendTicketEmail(user, ticket, payment)

class NewMovieNotificationObserver(Observer):
    def update(self, event_type, data):
        if event_type == 'new_movie':
            movie = data['movie']
            notifyNewMovie(movie)
