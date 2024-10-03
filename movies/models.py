from django.db import models

class Movie(models.Model):

    #generos pré definidos para facilitar na filtragem dos filmes depois
    GENRES=[
        ('None','None'),
        ('Action','Action'),
        ('Adventure','Adventure'),
        ('Animation','Animation'),
        ('Comedy','Comedy'),
        ('Drama','Drama'),
        ('Documentary','Documentary'),
        ('Fantasy','Fantasy'),
        ('Horror','Horror'),
        ('Mystery','Mystery'),
        ('Musical','Musical'),
        ('Romance','Romance'),
        ('Thriller','Thriller'),
        ('Sci-Fi','Sci-fi'),
        ('Superhero','Superhero'),
        ('Psychological Horror','Psychological Horror'),
    ]

    title=models.CharField(max_length=255)
    plot=models.CharField(max_length=1000)
    duration=models.IntegerField()
    genre1=models.CharField(max_length=20, choices=GENRES, default='None')
    genre2=models.CharField(max_length=20, choices=GENRES, blank=True, null=True, default='None')
    year=models.CharField(max_length=4)
    director=models.CharField(max_length=100)
    country=models.CharField(max_length=30)
    poster=models.URLField(blank=True, null=True)
    rating=models.IntegerField()
    trailer_url=models.URLField(blank=True, null=True)
    dateAdded=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title