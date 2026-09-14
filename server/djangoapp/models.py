from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(default=2023)

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


class Dealer(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, blank=True, default='')
    full_name = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=10, blank=True, default='')
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Review(models.Model):
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(default=now)
    car_make = models.CharField(max_length=100, blank=True, null=True)
    car_model = models.CharField(max_length=100, blank=True, null=True)
    car_year = models.IntegerField(blank=True, null=True)
    sentiment = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Review by {self.name} for dealer {self.dealer_id}"