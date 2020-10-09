from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import django.db.models.deletion
# Create your models here.

# class Owner(models.Model):
#     """Owner"""
#     name = models.CharField("Owner", max_length=150)
#     password = models.CharField(max_length=32)
#     email = models.EmailField()
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Owner"
#         verbose_name_plural = "Owners"


class Network(models.Model):
    """Lora Network"""
    name = models.CharField("Network", max_length=150)
    owner = models.ForeignKey(User, on_delete=models.deletion.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Networks"


class Getaway(models.Model):
    """Lora Getaway"""
    name = models.CharField("Getaway", max_length=150)
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180)])
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90)])
    network = models.ForeignKey(Network, models.deletion.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Getaway"
        verbose_name_plural = "Getaways"

class Node(models.Model):
    """Lora Node"""
    name = models.CharField("Node", max_length=150)
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180)])
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90)])
    charge = models.FloatField()
    active = models.BooleanField()
    getaway = models.ForeignKey(Getaway, models.deletion.CASCADE, related_name="nodes")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"


class Device(models.Model):
    """Device"""
    name = models.CharField("Device", max_length=150)
    units = models.CharField("units", max_length=10)
    node = models.ForeignKey(Node, models.deletion.CASCADE, related_name="devices")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"


class Device_info(models.Model):
    """Data from Device """
    date = models.DateTimeField()
    info = models.FloatField()
    device = models.ForeignKey(Device, models.deletion.CASCADE, related_name="dataList")

    def __str__(self):
        return str(self.device)

    class Meta:
        verbose_name = "Information"