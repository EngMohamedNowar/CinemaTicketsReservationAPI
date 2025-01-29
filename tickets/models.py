from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

User = settings.AUTH_USER_MODEL





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

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.title} by { self.author.username}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
