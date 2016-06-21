from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import View

from tickets.forms import TicketForm
from tickets.models import Ticket, SpecificItem, Item, Location


class IndexView(View):
    def get(self, request):
        context = {}
        return render(request, 'tickets/index.html', context)


class NewTicketView(View):
    context = {}

    @method_decorator(login_required)
    def get(self, request):
        self.context["form"] = TicketForm()

        return render(request, 'tickets/new.html', self.context)

    @method_decorator(login_required)
    def post(self, request):
        form = TicketForm(request.POST)

        valid = form.is_valid()
        if valid:

            specific_item = SpecificItem.objects.filter(item=Item.objects.get(id=form.data['item']),
                                                        location=Location.objects.get(id=form.data['location']))
            if specific_item.count() > 0:
                test = specific_item.first()

                ticket = Ticket(creator=request.user, description=form.cleaned_data['description'],
                                item=test)

                ticket.save()

                mail_body = 'Je hebt een ticket aangemaakt op het ticketsysteem \n' + \
                            ' bekijk de vooruitgang van je ticket op ' + '' \
                                                                         'ticketsysteem.guushamm.tech/tickets/view/{}'.format(
                    ticket.id)

                email = EmailMessage('Ticket#{} aangemaakt'.format(ticket.id), mail_body, to=[request.user.email])
                email.send()
                messages.success(request, "Ticket succesvol aangemaakt")
                return redirect("tickets:view", ticket_id=ticket.id)
            else:
                messages.info(request, "Het gekozen item bestaat niet op deze locatie")
                return render(request, 'tickets/new.html', self.context)

        else:
            messages.warning(request, "Whoops het formulier is niet goed ingevuld")
            return render(request, 'tickets/new.html', self.context)


class ViewTicketView(View):
    def get(self, request, ticket_id):
        context = {}

        context["ticket"] = get_object_or_404(Ticket, pk=ticket_id)

        return render(request, "tickets/view.html", context)


class MyTicketsView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {}

        context["tickets"] = Ticket.objects.filter(creator=request.user).order_by('created_at').reverse()

        return render(request, "tickets/tickets.html", context)
