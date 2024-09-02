from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from movies.models import Movie

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError("A data de nascimento não pode ser no futuro.")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.username}: {self.user.email}"


class Wallet(models.Model):
    profile=models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="wallet")
    balance=models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def add_balance(self, amount):
        if amount>0:
            self.balance+=amount
            self.save()
        else:
            raise ValueError("O valor para adicionar deve ser positivo.")

    def deduct_balance(self, amount):
        if amount>0:
            if self.balance>=amount:
                self.balance-=amount
                self.save()
            else:
                raise ValueError("Saldo insuficiente.")
        else:
            raise ValueError("O valor para deduzir deve ser positivo.")

    def __str__(self):
        return f"Wallet de {self.profile.user.username} - Saldo: {self.balance}"

class CreditCard(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="credit_cards")
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=100)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Cartão de Crédito - {self.card_holder} - Final {self.card_number[-4:]}"

class DebitCard(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="debit_cards")
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=100)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Cartão de Débito - {self.card_holder} - Final {self.card_number[-4:]}"
    

class Review(models.Model):
    RATE_CHOICES=[
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8),
        (9,9),
        (10,10),
    ]

    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
    rate=models.PositiveBigIntegerField(choices=RATE_CHOICES)
    comment=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=('movie','profile')

    def clean(self):
        if Review.objects.filter(movie=self.movie, profile=self.profile).exclude(id=self.id).exists():
            raise ValidationError("Voce já avaliou esse filme")
        super().clean()

    def __str__(self):
        return f"{self.profile} - {self.movie}"
