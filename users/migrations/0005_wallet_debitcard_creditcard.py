# Generated by Django 5.0.7 on 2024-08-20 20:20

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='DebitCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('card_holder', models.CharField(max_length=100)),
                ('expiration_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debit_cards', to='users.wallet')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('card_holder', models.CharField(max_length=100)),
                ('expiration_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_cards', to='users.wallet')),
            ],
        ),
    ]