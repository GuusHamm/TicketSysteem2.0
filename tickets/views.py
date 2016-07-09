from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from ticketsysteem import settings
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import View

from tickets.forms import TicketForm, ClaimSelectUserForm
from tickets.models import SpecificItem, Item, Location, Ticket


class IndexView(View):
    """
Server as a landing page.

**Context**

``number_of_tickets``
    The number of total tickets in the ticketsystem at any given time
``number_open_of_tickets``
    The number of open tickets in the ticketsystem at any given time

**Template:**

:template:`tickets/index.html`
"""

    def get(self, request):
        context = {}
        context["number_of_tickets"] = Ticket.objects.count()
        context["number_of_open_tickets"] = Ticket.objects.filter(assigned=False).exclude(status="CLOSED").count()

        return render(request, 'tickets/index.html', context)


class NewTicketView(View):
    """
Page to create a new ticket :model:`tickets.Ticket`,
 when the form is valid a mail will be sent to the ticket creator and site managers.


**Context**

``form``
    The TicketForm Form

**Template:**

:template:`tickets/new.html`
"""
    context = {}

    @method_decorator(login_required)
    def get(self, request):
        self.context["form"] = TicketForm()

        return render(request, 'tickets/new.html', self.context)

    @method_decorator(login_required)
    def post(self, request):
        form = TicketForm(request.POST)

        valid = form.is_valid()
        # first off all we check if the form is valid
        if valid:
            # This check's if the item the user has selected exists in the location.
            # This solution is not optimal but it works, The ideal solution would be to use AJAX
            specific_items = SpecificItem.objects.filter(item=Item.objects.get(id=form.data['item']),
                                                        location=Location.objects.get(id=form.data['location']))
            if specific_items.count() > 0:
                specific_item = specific_items.first()

                # We create the ticket here
                ticket = Ticket(creator=request.user, description=form.cleaned_data['description'],
                                item=specific_item, title=form.cleaned_data['title'])
                # And we save it, this will trigger the TicketHandler
                ticket.save()

                # We only want the system to send a mail when Debug is False, therefor we check it here
                if not settings.DEBUG:
                    mail_body = 'Je hebt een ticket aangemaakt op het ticketsysteem \n' + \
                                ' bekijk de vooruitgang van je ticket op ' + '' \
                                                                             'http://ticketsysteem.guushamm.tech/tickets/view/{}'.format(
                        ticket.id)

                    mail_subject = 'Ticket#{} aangemaakt'.format(ticket.id)

                    email = EmailMessage(mail_subject, mail_body, to=[request.user.email])
                    email.send()
                # If we get to this point we have succesfully created a ticket. So we let the user know that
                messages.success(request, "Ticket succesvol aangemaakt")
                return redirect("tickets:view", ticket_id=ticket.id)
            else:
                # If we get here the item is not on the chosen location, so we let the user know
                messages.info(request, "Het gekozen item bestaat niet op deze locatie")
                return render(request, 'tickets/new.html', self.context)

        else:
            # The form has not been correctly filled in, so we let the user know.
            messages.warning(request, "Whoops het formulier is niet goed ingevuld")
            return render(request, 'tickets/new.html', self.context)


class ViewTicketView(View):
    """
Shows a specific Ticket, :model:`tickets.Ticket`

**Context**

``ticket``
  The requested ticket
``form``
  The ClaimUserForm

**Template:**

:template:`tickets/index.html`
"""
    @method_decorator(login_required)
    def get(self, request, ticket_id):
        context = {}

        if request.user.is_superuser:
            context['form'] = ClaimSelectUserForm()

        ticket = get_object_or_404(Ticket, pk=ticket_id)
        if ticket.user_is_allowed_to_view(user=request.user):
            context["ticket"] = ticket
            return render(request, "tickets/view.html", context)
        else:
            messages.add_message(request, messages.ERROR, "You are not allowed to view this ticket")
            return render(request, 'tickets/index.html')

    @method_decorator(staff_member_required)
    def post(self, request, ticket_id):
        form = ClaimSelectUserForm(request.POST)

        user_id = form.data.get('user')

        if form.is_valid():
            return redirect('tickets:claim', ticket_id=ticket_id, user_id=user_id)


class MyTicketsView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {}

        if request.user.is_superuser:
            context["tickets"] = Ticket.objects.all().exclude(status="CLOSED").order_by('created_at').reverse()
        elif request.user.is_staff:
            context["tickets"] = Ticket.objects.filter(assigned_to=request.user).order_by('created_at').reverse()
        else:
            context["tickets"] = Ticket.objects.filter(creator=request.user).order_by('created_at').reverse()

        return render(request, "tickets/tickets.html", context)


class ClaimTicketView(View):
    @method_decorator(login_required)
    def get(self, request, ticket_id, user_id=-1):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if user_id == -1:
            user = request.user
        else:
            user = get_object_or_404(User, id=user_id)

        ticket.assigned_to = user
        ticket.save()

        messages.add_message(request, messages.SUCCESS,
                             '{} toegewezen aan ticket# {}'.format(user.first_name, ticket.id))

        return redirect('tickets:view', ticket_id=ticket_id)
