from django.core.management.base import BaseCommand
from counselor.models import *

import requests

from ecocloud.tools import load_csv


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_csv()

        services = requests.get("https://api.aiven.io/v1/service_types").json()

        for service_name in services["service_types"]:
            service_object = Service.objects.create(name=service_name)
            for region_name in services["service_types"][service_name]["service_plans"][0]["regions"]:
                region = Region.objects.filter(name=region_name)
                if not region.exists():
                    region = Region.objects.create(name=region_name)
                    print(region)
                else:
                    region = region.first()
                service_object.available_regions.add(region)
