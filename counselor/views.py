from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from counselor.serializers import RegionSerializer


class GetRankSuggestionAPIView(APIView):
    def get(self, request):
        service_name = request.GET.get('service')
        current_region_name = request.GET.get('region_name')

        if service_name is None:
            return Response("'service' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)

        if current_region_name is None:
            return Response("'region_name' parameter was not provided", status=status.HTTP_400_BAD_REQUEST)

        # function call

        response = {
            "rank": 1,
            "region_suggestion": RegionSerializer(many=True).data,
            "current_co": 1
        }

        return Response(response, status=status.HTTP_200_OK)
