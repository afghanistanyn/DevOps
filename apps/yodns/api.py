# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from yodns import models,serializers,filter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from yodns.permission import yodns as DNSPermission

class DNSPagination(PageNumberPagination):
    page_size = 10


class DNSListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all()
    permission_classes = [DNSPermission.DNSListRequiredMixin, IsAuthenticated]
    filter_class = filter.DNSFilter


class DNSListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all().exclude(father__isnull=True)
    permission_classes = [DNSPermission.DNSListRequiredMixin, IsAuthenticated]
    pagination_class = DNSPagination
    filter_class = filter.DNSFilter


class DNSCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all()
    permission_classes = [DNSPermission.DNSCreateRequiredMixin, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if 'father' in request.data:
            father = models.DNS.objects.get(id=request.data['father'])
            if father.sons.filter(name__in=[request.data['name'],]).exists():
                return Response({'detail':'域名树重复'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return super(DNSCreateAPI, self).create(request, *args, **kwargs)
        else:
            return super(DNSCreateAPI, self).create(request, *args, **kwargs)


class DNSUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all()
    permission_classes = [DNSPermission.DNSUpdateRequiredMixin, IsAuthenticated]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


class DNSDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all()
    permission_classes = [DNSPermission.DNSDeleteRequiredMixin, IsAuthenticated]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        dns_obj = self.get_object()
        if dns_obj.sons.exists():
            return Response({'detail':'该域名节点下存在子节点'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(DNSDeleteAPI, self).delete(request, *args, **kwargs)