from django.db import models

# Create your models here.


class Device(models.Model):
    name = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=20, unique=True, primary_key=True)


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=64)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null=True)
