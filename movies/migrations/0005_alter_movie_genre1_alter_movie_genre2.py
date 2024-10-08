# Generated by Django 5.0.7 on 2024-08-31 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_movie_trailer_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre1',
            field=models.CharField(choices=[('None', 'None'), ('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Documentary', 'Documentary'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Musical', 'Musical'), ('Romance', 'Romance'), ('Thriller', 'Thriller'), ('Sci-Fi', 'Sci-fi'), ('Superhero', 'Superhero'), ('Psychological Horror', 'Psychological Horror')], default='None', max_length=20),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre2',
            field=models.CharField(blank=True, choices=[('None', 'None'), ('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Documentary', 'Documentary'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Musical', 'Musical'), ('Romance', 'Romance'), ('Thriller', 'Thriller'), ('Sci-Fi', 'Sci-fi'), ('Superhero', 'Superhero'), ('Psychological Horror', 'Psychological Horror')], default='None', max_length=20, null=True),
        ),
    ]
