from rest_framework import serializers

from counselor.models import Region, ServiceRegionRelation
from ecocloud.tools import get_spec_co


class RegionSerializer(serializers.ModelSerializer):
    spec_co = serializers.SerializerMethodField()
    price_diff = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = [
            'provider',
            'name',
            'spec_co',
            'price_diff'
        ]

    def get_spec_co(self, obj):
        current_spec = self.context.get("spec")
        return get_spec_co(current_spec, obj)

    def get_price_diff(self, obj):
        service = self.context.get("service")
        service_plan = self.context.get("service_plan")
        relation = ServiceRegionRelation.objects.get(region=obj, service_plan=service_plan.service_plan,
                                                     service=service)
        return relation.price - service_plan.price
