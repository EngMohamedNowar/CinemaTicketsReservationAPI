from django.db import models


# Create your models here.

# Guest --  Movie -- Reservation
class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=11)

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie = models.CharField(max_length=50)
    hall = models.CharField(max_length=50)

    def __str__(self):
        return self.movie


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation by {self.guest.name} for {self.movie.movie}"

