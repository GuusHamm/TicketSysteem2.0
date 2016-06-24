from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission
from django.core.mail import EmailMessage
from django.db import models

# Create your models here.
from django.db.models import Q


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
        return "{}, {}".format(self.name, self.vendor.name)


class SpecificItem(models.Model):
    item = models.ForeignKey(Item)
    location = models.ForeignKey(Location)
    internal_id = models.CharField(max_length=255)

    def __str__(self):
        return "{}, {}".format(self.item.name, self.location.location)


class Ticket(models.Model):
    ticket_types = (("PROBLEM", "Probleem Oplossen"),
                    ("INSTALLATION", 'Instalatie'),
                    ("MAINTENANCE", 'Onderhoud'),
                    ("REINSTALL", "Herinstallatie"))
    ticket_statuses = (("OPEN", "Open"), ("IN PROGRESS", "In Behandeling"), ("CLOSED", "Gesloten"))

    ticket_type = models.CharField(max_length=255, choices=ticket_types, default='PROBLEM')
    creator = models.ForeignKey(User, related_name='creator')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField('creation date', auto_now_add=True)
    item = models.ForeignKey(SpecificItem)
    assigned = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, related_name='assigned_to', null=True, blank=True)
    assignment_date = models.DateField('assignment date', null=True, blank=True)
    status = models.CharField(max_length=255, choices=ticket_statuses, default="OPEN")

    def user_is_allowed_to_view(self, user):
        if self.creator == user or self.assigned_to == user or user.is_staff:
            return True
        else:
            return False

    def send_mail_users(self):
        permission = Permission.objects.get(codename='tickets.change_ticket')
        users = User.objects.filter((Q(groups__permissions=permission) | Q(user_permissions=permission)).distinct())

        for user in users:
            mail_body = 'Er is een ticket gemaakt: {}, {}, {} '.format(self.title, self.item, self.creator)

            email = EmailMessage('Ticket#{} aangemaakt'.format(self.id), mail_body, to=[user.email])
            email.send()

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')


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
