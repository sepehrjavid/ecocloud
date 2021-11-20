from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from counselor.models import Service, Region
from counselor.serializers import RegionSerializer
from ecocloud.tools import get_region_rank


class GetRankSuggestionAPIView(APIView):
    def get(self, request):
        service_name = request.GET.get('service')
        current_region_name = request.GET.get('region_name')

        if service_name is None:
            return Response("'service' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)

        if current_region_name is None:
            return Response("'region_name' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)

        service_object = get_object_or_404(Service, name=service_name)
        current_region = get_object_or_404(Region, name=current_region_name)

        suggestion, current_rank = get_region_rank(service_object.available_regions, current_region)

        response = {
            "rank": current_rank,
            "region_suggestion": RegionSerializer(suggestion, many=True).data,
            "spec_co": 1
        }

        return Response(response, status=status.HTTP_200_OK)
