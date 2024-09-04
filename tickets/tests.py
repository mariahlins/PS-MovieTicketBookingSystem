from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile
from movies.models import Movie
from .models import Ticket, Session, Coupon
from decimal import Decimal
from cinemas.models import Cinema, Room

class TicketModelTest(TestCase):

    def setUp(self):
        self.user=User.objects.create_user(username='testuser', password='12345')
        self.profile=Profile.objects.create(user=self.user, birth_date='2004-09-06')
        self.movie=Movie.objects.create(title="Test Movie", duration=120, rating=10)
        self.cinema=Cinema.objects.create(cinemaName='testcine', state="TE", city="Test City", rooms=3)
        self.room=Room.objects.create(cinema=self.cinema, roomNumber=1, seats=30)
        self.session = Session.objects.create(movie=self.movie, date="2024-09-01", hour="18:00", price=25, cinema=self.cinema, room=self.room, available_seats=30)
        self.ticket = Ticket.objects.create(
            session=self.session,
            user=self.profile,
            price=25,
            seatNumber="1",
            status="PENDING",
            ticketType='NORMAL',
        )
        self.coupon = Coupon.objects.create(code='DISCOUNT10', discount=10, active=True, validFrom="2024-01-01",validUntil="2024-12-31")

    def testTicketReserve(self):
        #reserva um ticket 
        self.ticket.reserve(self.profile, self.ticket.ticketType)
        self.assertEqual(self.ticket.status, 'PENDING')

    def testTicketCancel(self):
        #reserva e cancela (usa os atributos da propria classe)
        self.ticket.reserve(self.profile, self.ticket.ticketType)
        self.ticket.cancel()
        #quando eu cancelo, ele tem q ser liberado
        self.assertEqual(self.ticket.status, 'FREE')

    def testTicketPriceDiscount(self):
        #testa o desconto no ticket
        self.ticket.apply_coupon("DISCOUNT10")
        #10% de desconto nos 25 do preço do ingresso (25-2.5)
        self.assertEqual(self.ticket.price, Decimal('22.5'))
