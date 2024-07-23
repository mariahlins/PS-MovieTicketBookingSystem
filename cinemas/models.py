from django.db import models

class Cinema(models.Model):

    BRAZILIAN_STATES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]

    cinemaName=models.CharField(max_length=40)
    state=models.CharField(max_length=2, choices=BRAZILIAN_STATES)
    city=models.CharField(max_length=40)
    rooms=models.IntegerField()
    dateAdded=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.cinemaName} - {self.state}"
    

class Room(models.Model):
    cinema=models.ForeignKey(Cinema, on_delete=models.CASCADE)
    roomNumber=models.IntegerField()
    seats=models.IntegerField()
    dateAdded=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sala {self.roomNumber}"