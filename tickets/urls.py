from django.conf.urls import url

from tickets.views import IndexView, MyTicketsView, ViewTicketView, NewTicketView

urlpatterns = [
    url(r"^new/", NewTicketView.as_view(), name="new"),
    url(r"^view/(?P<ticket_id>\d+)", ViewTicketView.as_view(), name="view"),
    url(r"^mytickets/", MyTicketsView.as_view(), name="mytickets"),
    url(r'^$', IndexView.as_view(), name="index"),
]
