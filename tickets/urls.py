from django.conf.urls import url

from tickets.views import IndexView, MyTicketsView, ViewTicketView, NewTicketView, ClaimTicketView

urlpatterns = [
    url(r"^new/", NewTicketView.as_view(), name="new"),
    url(r"^view/(?P<ticket_id>\d+)", ViewTicketView.as_view(), name="view"),
    url(r"^mytickets/", MyTicketsView.as_view(), name="my_tickets"),
    url(r'^claim/(?P<ticket_id>\d+)/(?P<user_id>\d+)', ClaimTicketView.as_view(), name='claim'),
    url(r'^claim/(?P<ticket_id>\d+)', ClaimTicketView.as_view(), name='claim'),
    url(r'^$', IndexView.as_view(), name="index"),
]
