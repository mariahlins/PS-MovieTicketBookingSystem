# Generated by Django 5.0.7 on 2024-08-03 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_remove_movie_genre_delete_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genre1',
            field=models.CharField(choices=[('None', 'None'), ('Action', 'Action'), ('Adventure', 'Adventure'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Documentary', 'Documentary'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Musical', 'Musical'), ('Romance', 'Romance'), ('Thriller', 'Thriller'), ('Sci-Fi', 'Sci-fi'), ('Superhero', 'Superhero'), ('Psychological Horror', 'Psychological Horror')], default='None', max_length=20),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre2',
            field=models.CharField(blank=True, choices=[('None', 'None'), ('Action', 'Action'), ('Adventure', 'Adventure'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Documentary', 'Documentary'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Musical', 'Musical'), ('Romance', 'Romance'), ('Thriller', 'Thriller'), ('Sci-Fi', 'Sci-fi'), ('Superhero', 'Superhero'), ('Psychological Horror', 'Psychological Horror')], default='None', max_length=20, null=True),
        ),
    ]
