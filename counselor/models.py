from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=200)
    co_foot_print = models.IntegerField(null=True)
    pue = models.IntegerField(null=True)


class Service(models.Model):
    name = models.CharField(max_length=100)
    available_regions = models.ManyToManyField(Region, blank=True)
