from django.core.management.base import BaseCommand
from counselor.models import *

import requests

from ecocloud.tools import load_csv

CONTINENTS = ["asia", "north america", "europe", "south america", "africa"]


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_csv()

        regions = requests.get("https://api.aiven.io/v1/clouds").json()

        for region in regions["clouds"]:
            region_object = Region.objects.filter(name=region["cloud_name"])
            if not region_object.exists():
                if "do" not in region["cloud_name"] and "upcloud" not in region["cloud_name"]:
                    country = region["cloud_description"].lower().split(',')[0]
                if country in CONTINENTS:
                    country = region["cloud_description"].lower().split(',')[1][1:].split('-')[0][:-1]
                Region.objects.create(name=region["cloud_name"], continent=region["geo_region"], country=country)

        services = requests.get("https://api.aiven.io/v1/service_types").json()

        for service_name in services["service_types"]:
            service_object = Service.objects.create(name=service_name)
            for service_plan in services["service_types"][service_name]["service_plans"]:
                service_plan_name = service_plan["service_plan"]
                for region_name in service_plan["regions"]:
                    region = Region.objects.filter(name=region_name).first()
                    ServiceRegionRelation.objects.create(
                        region=region, service=service_object,
                        service_plan=service_plan_name,
                        price=float(service_plan["regions"][region_name]["price_usd"]) * 730
                    )
