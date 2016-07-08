from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.contrib.auth.models import User

from tickets.models import Location, Item


class TicketForm(forms.Form):
    ticket_types = (("PROBLEM", "Probleem oplossen"),
                    ("INSTALLATION", 'Instalatie'),
                    ("MAINTENANCE", 'Onderhoud'))

    type = forms.ChoiceField(choices=ticket_types)
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea(), max_length=255)
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    location = forms.ModelChoiceField(queryset=Location.objects.all())

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("type"),
            Field("title", placeholder="Bijvoorbeeld: computer start niet op"),
            Field("description"),
            Field("item"),
            Field("location"),

            FormActions(
                Submit('post', 'Post', css_class=" btn-danger btn-block"),
            )
        )


class ClaimSelectUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), label="Kies een gebruiker")

    def __init__(self, *args, **kwargs):
        super(ClaimSelectUserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("user"),

            FormActions(
                Submit('select_user', 'Kies gebruiker', css_class=" btn-danger btn-block"),
            )
        )
