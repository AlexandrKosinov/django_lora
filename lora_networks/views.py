from django.contrib.auth.models import User
from django.views.generic.base import View
from rest_framework import permissions

from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from lora_networks.models import Network, Getaway, Node, Device, Device_info
from lora_networks.serializers import LoraNetworkListSerializer, LoraGetawayListSerializer, \
    LoraNodeListSerializer, LoraDeviceListSerializer, LoraDeviceInfoListSerializer, LoraUserIdSerializer


# class OwnersView(APIView):
#
#     def get(self, request):
#         owners = Owner.objects.all()
#         serialazer = OwnerListSerializer(owners, many=True)
#         return Response(serialazer.data)

class LoadUserId(APIView):

    def get(self, request, user_name):
        userId = User.objects.filter(username=user_name)
        serialazer = LoraUserIdSerializer(userId, many=True)
        return Response(serialazer.data)

class LoraNetworkListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, owner_id):
        networks = Network.objects.filter(owner=owner_id)
        serialazer = LoraNetworkListSerializer(networks, many=True)
        return Response(serialazer.data)


class LoraGetawayListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, network_id):
        getaways = Getaway.objects.filter(network=network_id)
        serialazer = LoraGetawayListSerializer(getaways, many=True)
        return Response(serialazer.data)


class LoraNodeListView(APIView):

    def get(self, request, getaway_id):
        nodes = Node.objects.filter(getaway=getaway_id)
        serialazer = LoraNodeListSerializer(nodes, many=True)
        return Response(serialazer.data)


class LoraDeviceListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, node_id):
        devices = Device.objects.filter(node=node_id)
        serialazer = LoraDeviceListSerializer(devices, many=True)
        return Response(serialazer.data)


class LoraGetawayNodesListView(APIView):

    def get(self, request, network_id):
        getaways = Getaway.objects.filter(network=network_id)
        nodes = []
        for getaway in getaways:
            gnodes = Node.objects.filter(getaway=getaway.id)
            nodes.extend(gnodes)
        nodes.sort(key=lambda x: x.getaway.id, reverse=False)
        serialazer = LoraNodeListSerializer(nodes, many=True)
        return Response(serialazer.data)


class LoraDeviceInfoListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, dev_id):
        devInfo = Device_info.objects.filter(device=dev_id)
        serialazer = LoraDeviceInfoListSerializer(devInfo, many=True)
        return Response(serialazer.data)