from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal


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
