from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from movies.models import Movie
from .models import Profile, Wallet

class ProfileModelTest(TestCase):

    def setUp(self):
        #cria um usuário para os testes
        self.user=User.objects.create_user(username='testuser', password='12345')
        self.profile=Profile.objects.create(user=self.user, birth_date='2004-09-06')

    def testBirthDate(self):
        #a data de nascimento há de ser anterior à atual
        futureDate=timezone.now().date() + timezone.timedelta(days=1)
        self.profile.birth_date=futureDate
        #espera um erro de data de nascimento inválida
        with self.assertRaises(ValidationError):
            self.profile.clean()

    def testProfileRepresentation(self):
        #teste para conferir se a representação que eu defini está sendo atendida
        self.assertEqual(str(self.profile), f'{self.user.first_name} {self.user.username}: {self.user.email}')

    def testProfileDefaultReceiveNotifications(self):
        #testa se o padrão de receive_movie_notifications é True
        self.assertTrue(self.profile.receive_movie_notifications)

class WalletModelTest(TestCase):

    def setUp(self):
        self.user=User.objects.create_user(username='testuser', password='12345')
        self.profile=Profile.objects.create(user=self.user, birth_date='2004-09-06')
        self.wallet=Wallet.objects.create(profile=self.profile, balance=Decimal('100.00'))

    #testar os metodos da classe Wallet
    def testAddBalance(self):
        self.wallet.add_balance(Decimal('50.00'))
        self.assertEqual(self.wallet.balance, Decimal('150.00'))

    def testDeductBalance(self):
        self.wallet.deduct_balance(Decimal('50.00'))
        self.assertEqual(self.wallet.balance, Decimal('50.00'))

    def testDeductBalanceInsufficient(self):
        with self.assertRaises(ValueError):
            self.wallet.deduct_balance(Decimal('200.00'))

    def testAddBalanceNegative(self):
        with self.assertRaises(ValueError):
            self.wallet.add_balance(Decimal('-50.00'))

    def testDeductBalanceNegative(self):
        with self.assertRaises(ValueError):
            self.wallet.deduct_balance(Decimal('-50.00'))
