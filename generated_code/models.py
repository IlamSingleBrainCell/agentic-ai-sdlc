from django.db import models

class Flight(models.Model):
    """
    Model representing a flight.
    """
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    date = models.DateField()
    airline = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stops = models.IntegerField()

    def __str__(self):
        return f"{self.origin} to {self.destination} on {self.date}"