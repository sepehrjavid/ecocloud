from django.db import models

# all info about a single datacenter
class Region(models.Model):
    # this is in the format provider-region. eg: aws-us-central
    name = models.CharField(unique=True, max_length=200)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=50)
    # tons of co2 equivalent per kWh used by the datacenter
    co_foot_print = models.FloatField(null=True)
    # power usage effectiveness
    #   - all energy used by the datacenter/ energy used by the servers and computer
    #       hardware
    #   - basically how much energy the datacenter wastes for things that are not
    #       computers
    pue = models.FloatField(null=True)

    def __str__(self):
        return self.name

    # get only the provider (aws/google/azure)
    @property
    def provider(self):
        return self.name.split('-')[0]


# the different services that aiven offers (postgresql/mysql/kafka)
class Service(models.Model):
    name = models.CharField(max_length=100)
    # the regions where this service is offered
    available_regions = models.ManyToManyField(Region, blank=True, through='ServiceRegionRelation')

    def __str__(self):
        return self.name


# connecting the services to all the region objects where it's available
class ServiceRegionRelation(models.Model):
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='plan')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='plan')
    service_plan = models.CharField(max_length=60)
    price = models.IntegerField()

    class Meta:
        unique_together = ('region', 'service', 'service_plan')
