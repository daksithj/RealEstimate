from django.db import models
from django.utils import timezone


class RawLandData(models.Model):
    price = models.IntegerField(default = 0, null = True)
    price_type = models.CharField(max_length=10, null = True)
    location1 = models.CharField(max_length=30, null = True)
    location2 = models.CharField(max_length=30, null = True)
    land_type = models.CharField(max_length=20, null = True)
    land_size = models.FloatField(default = 0, null = True)
    size_type = models.CharField(max_length =20, null = True)
    land_availability = models.CharField(max_length=20, null = True)
    heading = models.TextField(null = True)
    about = models.TextField(null = True)
    date_collected= models.DateTimeField(default= timezone.now, null = True)

    def __str__(self):
        return self.id

class RawHouseData(models.Model):
    price = models.IntegerField(default = 0, null = True)
    #price_type = models.CharField(max_length=10, null = True)
    location1 = models.CharField(max_length=30, null = True)
    location2 = models.CharField(max_length=30, null = True)
    bedrooms = models.IntegerField(default=1, null=True)
    bathrooms= models.IntegerField(default=1, null=True)
    floor_area = models.IntegerField(default=0, null=True)
    floors = models.IntegerField(default=1, null=True)
    parking = models.IntegerField(default=0, null=True)
    property_type = models.CharField(max_length=20, null = True)
    land_size = models.FloatField(default = 0, null = True)
    land_availability = models.CharField(max_length=20, null = True)
    heading = models.TextField(null = True)
    about = models.TextField(null = True)
    features = models.TextField(null=True)
    date_collected= models.DateTimeField(default= timezone.now, null = True)

    def __str__(self):
        return self.id




