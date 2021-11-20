from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from counselor.models import Service, Region, ServiceRegionRelation
from counselor.serializers import RegionSerializer
from counselor.services import Spec
from ecocloud.tools import get_region_rank, get_spec_co


class GetRankSuggestionAPIView(APIView):
    def get(self, request):
        service_name = request.GET.get('service')
        current_region_name = request.GET.get('region_name')
        nodes = request.GET.get('nodes')
        memory = request.GET.get('memory')
        storage = request.GET.get('storage')
        service_plane_name = request.GET.get('service_plane_name')
        cpu = request.GET.get('cpu')

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
        if service_plane_name is None:
            return Response("'service_plane_name' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)
        if cpu is None:
            return Response("'cpu' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)

        service_object = get_object_or_404(Service, name=service_name)
        current_region = get_object_or_404(Region, name=current_region_name)
        service_plan = get_object_or_404(ServiceRegionRelation, service_plan=service_plane_name, region=current_region,
                                         service=service_object)

        suggestion, current_rank = get_region_rank(
            service_object.available_regions.filter(pue__isnull=False, co_foot_print__isnull=False,
                                                    plan__service_plan=service_plan.service_plan).distinct(),
            current_region)
        current_spec = Spec(nodes=nodes, memory=memory, storage=storage, provider=current_region.provider)

        response = {
            "rank": current_rank,
            "region_suggestion": RegionSerializer(
                suggestion, many=True,
                context={"spec": current_spec, "service_plan": service_plan, "service": service_object}
            ).data,
            "spec_co": get_spec_co(current_spec, current_region)
        }

        return Response(response, status=status.HTTP_200_OK)


class GetLiveCoEmissionAPIView(APIView):
    def get(self, request):
        pass
