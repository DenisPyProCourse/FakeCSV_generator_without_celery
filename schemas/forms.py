from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from django_filters import FilterSet
from schemas.models import Schema, Columns


class UserRegistrationForm(UserCreationForm):
    """
    Simple user registration form
    """
    class Meta(UserCreationForm.Meta):
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class ColumnsForm(forms.ModelForm):
    """
    Form for Formset Schema columns
    """

    def __init__(self, *args, **kwargs):
        super(ColumnsForm, self).__init__(*args, **kwargs)

    class Meta:

        model = Columns
        exclude = ()


ColumnsFormSet = inlineformset_factory(
    Schema, Columns, form=ColumnsForm,
    fields="__all__",
    extra=1,
    can_delete=True,
    widgets={
        "cl_type": forms.Select(attrs={'onchange': 'foo(this.id)'}),
        }
    )


class SchemaCreateForm(forms.ModelForm):
    """
    Crispy Schema Creation Form
    """

    class Meta:
        model = Schema
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super(SchemaCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                Field('sep'),
                Field('str_char'),
                Fieldset('Add columns',
                         Formset('columns')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )


class SchemaFilterForm(FilterSet):
    """
    Form for list view
    """
    class Meta:
        model = Schema
        fields = {
            'id': ['exact'],
            'title': ['startswith'],
        }


class DatasetCreateForm(forms.Form):
    rows = forms.IntegerField(label="Rows", required=True)
