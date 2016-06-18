from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Location(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.TextField(max_length=255)

    description = models.TextField(max_length=255)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.name


class SpecificItem(models.Model):
    item = models.ForeignKey(Item)
    location = models.ForeignKey(Location)
    internal_id = models.CharField(max_length=255)

    def __str__(self):
        return "{}, {}".format(self.item.name, self.location.location)


class Ticket(models.Model):
    creator = models.ForeignKey(User, related_name='creator')
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField('creation date', auto_now_add=True)
    item = models.ForeignKey(SpecificItem)
    assigned = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, related_name='assigned_to', null=True, blank=True)
    assignment_date = models.DateField('assignment date', auto_now=True, null=True, blank=True)


class Part(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)

    vendor = models.ForeignKey(Vendor)
    supplier = models.CharField(max_length=255)
    indicated_price = models.DecimalField

    def __str__(self):
        return self.name


class ServiceContract(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    internal_id = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    expiry_date = models.DateField('expiry date', auto_now=True)

    def __str__(self):
        return self.name
