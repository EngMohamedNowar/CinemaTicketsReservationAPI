from django.db import models

# Create your models here.

# Guest --  Movie -- Reservation

class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)

class Movie(models.Model):
    name = models.CharField(max_length=50)
    hall = models.CharField(max_length=50)
    date = models.DateField()

class Reservation(models.Model):
    guest = models.ForeignKey(Guest,related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)
