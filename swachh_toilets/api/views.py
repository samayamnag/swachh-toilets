from rest_framework import generics
from rest_framework.response import Response
from swachh_toilets.models import SwachhToilet
from .authentication import CustomAuthentication
from swachh_toilets.api.serializers import ToiletSerializer
from .pagination import StandardResultsSetPageNumberPagination


class ToiletList(generics.ListAPIView):
    authentication_classes = (CustomAuthentication,)
    serializer_class = ToiletSerializer
    pagination_class = StandardResultsSetPageNumberPagination

    def get_queryset(self):
        coordinates = [
            float(self.request.GET.get('longitude')),
            float(self.request.GET.get('latitude'))
        ]

        """
        from .authentication import Profile
        profile = Profile().get_user_profile(
                    self.request,
                    self.request.user['id']
                    )
        coordinates = profile['location']['coordinates']
        """
        queryset = SwachhToilet.objects(
                    location__near=coordinates,
                    location__max_distance=1000
                )
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(qci_id__icontains=q)
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # result = [ x.values()[0] for x in serializer.data ]
        return Response(serializer.data)


class ToiletDetail(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = ToiletSerializer
    queryset = SwachhToilet.objects.all()
