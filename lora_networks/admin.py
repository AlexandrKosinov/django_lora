from django.contrib import admin
from .models import Network, Getaway, Node, Device, Device_info

admin.site.register(Network)
admin.site.register(Getaway)
admin.site.register(Node)
admin.site.register(Device)
admin.site.register(Device_info)
