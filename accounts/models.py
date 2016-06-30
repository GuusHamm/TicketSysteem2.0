# Create your models here.
from django.contrib.auth.models import User
from django.core.mail import mail_managers
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_handler(instance, created, **kwargs):
    if created and not instance.is_active:
        mail_managers(
            '{} {} heeft een account aangemaakt op het ticketsysteem'.format(instance.first_name, instance.last_name),
            '{} heeft een account aangemaakt op het ticketsysteem\n'.format(instance.first_name) +
            'activeer de account op de volgende link' +
            ' http://ticketsysteem.guushamm.tech/admin/auth/user/{}/change/'.format(instance.id))
