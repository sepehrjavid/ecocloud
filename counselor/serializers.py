from rest_framework import serializers

from counselor.models import Region
from ecocloud.tools import get_spec_co


class RegionSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()
    spec_co = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = [
            'provider',
            'name',
            'spec_co',
            'pue'
        ]

    def get_provider(self, obj):
        return obj.name.split('-')[0]

    def get_spec_co(self, obj):
        current_spec = self.context.get("spec")
        return get_spec_co(current_spec, obj)
