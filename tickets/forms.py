from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms

from tickets.models import SpecificItem


class TicketForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(), max_length=255)
    item = forms.ModelChoiceField(queryset=SpecificItem.objects.all())

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("description"),
            Field("item"),

            FormActions(
                Submit('post', 'Post', css_class=" btn-danger btn-block"),
            )
        )
