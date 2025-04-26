from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import CounselingCenter
from .serializers import CounselingCenterSerializer

class CounselingCenterListView(APIView):
    def get(self, request):
        region = request.query_params.get('region', '')
        keyword = request.query_params.get('keyword', '')
        fields = request.query_params.get('fields', '')

        centers = CounselingCenter.objects.all()

        if region:
            centers = centers.filter(region__icontains=region)

        if keyword:
            centers = centers.filter(name__icontains=keyword)

        if fields:
            field_list = fields.split(",")
            query = Q()
            for field in field_list:
                query |= Q(category__icontains=field)
            centers = centers.filter(query)

        serializer = CounselingCenterSerializer(centers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
