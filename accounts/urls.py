from django.conf.urls import url

from .views import *

urlpatterns = [
    # url(r'^', IndexView.as_view(), name="index")
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),
    url(r'^new/', CreateNewAccountView.as_view(), name="register"),
]
