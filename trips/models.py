from django.db import models

class Trip(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.origin} → {self.destination}"
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name