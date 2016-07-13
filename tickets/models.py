from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User, Permission
from django.core.mail import mail_managers, EmailMessage
from django.db import models
from django.utils import timezone

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from ticketsysteem import settings


class Location(models.Model):
    """
    Stores a location i.e. Service Desk
    """
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location


class Vendor(models.Model):
    """
    Stores a vendor i.e. Fujitsu
    """
    name = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ServiceContract(models.Model):
    """
   Stores a service contract,  i.e. Fujitsu Printer Service Contract.
   Related to :model:`tickets.Item`
   """
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    internal_id = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    expiry_date = models.DateField('expiry date', auto_now=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Stores a item,  i.e. Fujitsu Desktop Computer.
    Related to :model:`tickets.Vendor`
    """
    name = models.TextField(max_length=255)

    description = models.TextField(max_length=255)
    vendor = models.ForeignKey(Vendor)
    service_contract = models.ForeignKey(ServiceContract, null=True, blank=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.vendor.name)


class Part(models.Model):
    """
    Stores a part,  i.e. Fujitsu Printer Cartridge.
    Related to :model:`tickets.Vendor`
    """
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    item = models.ForeignKey(Item)

    vendor = models.ForeignKey(Vendor)
    supplier = models.CharField(max_length=255)
    indicated_price = models.DecimalField

    def __str__(self):
        return self.name


class SpecificItem(models.Model):
    """
    Is a specific item at a department, i.e. a Fujitsu Desktop Computer at the Service Desk.
    Related to :model:`tickets.Item` and :model:`tickets.Location`
    """
    item = models.ForeignKey(Item)
    location = models.ForeignKey(Location)
    internal_id = models.CharField(max_length=255)

    def __str__(self):
        return "{}, {}".format(self.item.name, self.location.location)


class Ticket(models.Model):
    """
   Is a Ticket i.e. my computer is not booting.
   Has a type describing what kind of ticket it is.
   Has a status describing what the status of the ticket is.
   Related to :model:`tickets.SpecificItem` and :model:`auth.User`
   """
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
    assignment_date = models.DateTimeField('assignment date', null=True, blank=True)
    status = models.CharField(max_length=255, choices=ticket_statuses, default="OPEN")
    closed_at = models.DateTimeField('close date', null=True, blank=True)

    def time_open(self):
        """ Calculates the time a ticket has been open """
        diff = 0

        if self.status != 'CLOSED':
            diff = timezone.now() - self.created_at
        else:
            diff = self.closed_at - self.created_at

        suffix = ' dagen'

        if diff.days == 1:
            suffix = ' dag'

        return diff.days.__str__() + suffix

    def user_is_allowed_to_view(self, user):
        """ Checks whether a user is allowed to view the ticket i.e. user is creator, assignee or staff """
        if self.creator == user or self.assigned_to == user or user.is_staff:
            return True
        else:
            return False

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')


@receiver(post_save, sender=Ticket)
def ticket_handler(instance, created, **kwargs):
    if created:
        mail_managers('Ticket #{} aangemaakt'.format(instance.id),
                      'Er is een ticket gemaakt: {}, {}, {} '.format(instance.title, instance.item, instance.creator))
    else:
        if instance.assigned_to is not None and (not instance.assigned or not instance.assignment_date):
            instance.assigned = True
            instance.assignment_date = datetime.now()

            if not settings.DEBUG:
                email = EmailMessage("{} is toegewezen aan je ticket".format(instance.assigned_to.first_name),
                                     "{} is toegewezen aan je ticket".format(instance.assigned_to.first_name),
                                     to=[instance.creator.email])
                email.send()

                email = EmailMessage("Je bent toegewezen aan ticket #{}".format(instance.id),
                                     "Je bent toegewezen aan ticket #{}\n\n" +
                                     "Bekijk de ticket op ticketsysteem.guushamm.tech/tickets/view/{}".format(
                                         instance.id,
                                         instance.id),
                                     to=[instance.assigned_to.email])
                email.send()

            instance.save()
