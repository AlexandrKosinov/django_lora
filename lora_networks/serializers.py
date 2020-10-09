from django.contrib.auth.models import User
from rest_framework import serializers

from lora_networks.models import Network, Getaway, Node, Device, Device_info


# class OwnerListSerializer(serializers.ModelSerializer):
#     # *** owners ***
#
#     class Meta:
#         model = Owner
#         fields = ("__all__")

class LoraUserIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id']

class LoraNetworkListSerializer(serializers.ModelSerializer):
    # *** owner networks list ***

    class Meta:
        model = Network
        fields = ("__all__")


class LoraNodeListSerializer(serializers.ModelSerializer):
    # *** network nodes list ***owner

    class Meta:
        model = Node
        fields = ("__all__")


class LoraGetawayListSerializer(serializers.ModelSerializer):
    # *** network gataways list ***
    nodes = LoraNodeListSerializer(many=True)
    class Meta:
        model = Getaway
        fields = ("__all__")


class LoraDeviceListSerializer(serializers.ModelSerializer):
    # *** network devices list ***

    class Meta:
        model = Device
        fields = ("__all__")


class LoraDeviceInfoListSerializer(serializers.ModelSerializer):
    # *** network devices list ***

    class Meta:
        model = Device_info
        fields = ("__all__")


class CreateDeviceInfoSerializer(serializers.ModelSerializer):
    # *** network devices list ***

    class Meta:
        model = Device_info
        fields = ("date", "info", "device")

    def create(self, data):
        dataSensor = Device_info.objects.create(date=data.get("date"), info=data.get("info"), device=data.get("device"))
        return dataSensor