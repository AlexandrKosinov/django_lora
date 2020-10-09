from django.contrib import admin
from .models import Network, Getaway, Node, Device, Device_info

# Register your models here.


# admin.site.register(Owner)
admin.site.register(Network)
admin.site.register(Getaway)
admin.site.register(Node)
admin.site.register(Device)
admin.site.register(Device_info)
