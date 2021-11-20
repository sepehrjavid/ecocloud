from django.db import models


class Region(models.Model):
    name = models.CharField(unique=True, max_length=200)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=50)
    co_foot_print = models.IntegerField(null=True)
    pue = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    available_regions = models.ManyToManyField(Region, blank=True, related_name='services')

    def __str__(self):
        return self.name
