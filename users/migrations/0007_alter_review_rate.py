# Generated by Django 5.0.7 on 2024-09-02 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.PositiveBigIntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)]),
        ),
    ]
