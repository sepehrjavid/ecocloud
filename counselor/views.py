from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from counselor.models import Service, Region
from counselor.serializers import RegionSerializer
from counselor.services import Spec
from ecocloud.tools import get_region_rank, get_spec_power_use


class GetRankSuggestionAPIView(APIView):
    def get(self, request):
        service_name = request.GET.get('service')
        current_region_name = request.GET.get('region_name')
        nodes = request.GET.get('nodes')
        memory = request.GET.get('memory')
        storage = request.GET.get('storage')

        if service_name is None:
            return Response("'service' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)
        if current_region_name is None:
            return Response("'region_name' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)
        if nodes is None:
            return Response("'nodes' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)
        if memory is None:
            return Response("'memory' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)
        if storage is None:
            return Response("'storage' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)

        service_object = get_object_or_404(Service, name=service_name)
        current_region = get_object_or_404(Region, name=current_region_name)

        suggestion, current_rank = get_region_rank(service_object.available_regions, current_region)
        current_spec = Spec(nodes=nodes, memory=memory, storage=storage)

        response = {
            "rank": current_rank,
            "region_suggestion": RegionSerializer(suggestion, many=True, context={"spec": current_spec}).data,
            "spec_co": get_spec_power_use(current_spec)
        }

        return Response(response, status=status.HTTP_200_OK)
