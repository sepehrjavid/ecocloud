from rest_framework import serializers

from counselor.models import Region


class RegionSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = [
            'provider',
            'name',
            'co_foot_print',
            'pue'
        ]

    def get_provider(self, obj):
        return obj.name.split('-')[0]
