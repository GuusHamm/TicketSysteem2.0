from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r"^new", NewTicketView.as_view(), name="new"),
    url(r"^view/(?P<ticket_id>\d+)", ViewTicketView.as_view(), name="view"),
    url(r'^', IndexView.as_view(), name="index"),
]
