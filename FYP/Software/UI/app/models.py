from django.db import models
from . import ConnectionManager
# Create your models here.
import asyncio
from time import sleep


class Action(models.Model):

    class Actions(models.TextChoices):
        STANDING = 'Standing'
        WALKING = 'Walking'
        LYING_F = 'Lying Forwards'
        LYING_L = 'Lying Left'
        LYING_R = 'Lying Right'
        FALL_F = 'Fall Forwards'
        FALL_L = 'Fall Left'
        FALL_R = 'Fall Right'

    class Risk(models.IntegerChoices):
        LOW = 0
        MEDIUM = 1
        HIGH = 2

    name = models.CharField(max_length=50, choices=Actions.choices, unique=True)
    risk = models.IntegerField(choices=Risk.choices)

    def __str__(self):
        return self.name


class Device(models.Model):
    class Status(models.IntegerChoices):
        DISCONNECTED = 0, 'Disconnected'
        CONNECTING = 1, 'Connecting'
        CONNECTED = 2, 'Connected'
        STREAMING = 3, 'Streaming'

    cm = ConnectionManager()
    name = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=20, unique=True, primary_key=True)
    status = models.IntegerField(choices=Status.choices, default=Status.DISCONNECTED)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, default=1)


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=64)
    device = models.OneToOneField(Device, on_delete=models.CASCADE, blank=True, null=True, unique=True)
