from django.db import models


class Region(models.Model):
    name = models.CharField(unique=True, max_length=200)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=50)
    # tons of co2 eq per kWh used by the datacenter
    co_foot_print = models.FloatField(null=True)
    # power usage effectiveness
    # all energy used by the datacenter/ energy used by the servers and computer
    #   hardware
    # basically how much energy the datacenter wastes for things that are not
    #   computers
    pue = models.FloatField(null=True)

    def __str__(self):
        return self.name

    @property
    def provider(self):
        return self.name.split('-')[0]


class Service(models.Model):
    name = models.CharField(max_length=100)
    available_regions = models.ManyToManyField(Region, blank=True, through='ServiceRegionRelation')

    def __str__(self):
        return self.name


class ServiceRegionRelation(models.Model):
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='plan')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='plan')
    service_plan = models.CharField(max_length=60)
    price = models.IntegerField()

    class Meta:
        unique_together = ('region', 'service', 'service_plan')

    def __str__(self):
        return f"{self.region.name} | {self.service.name} | {self.service_plan} | {self.price}"
