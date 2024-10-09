from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, Field

from sentinel.utils.models import Province
from .models import Office


class OfficeForm(forms.ModelForm):

    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select())

    class Meta:
        model = Office
        fields = (
            'name', 'code', 'address', 'province', 'city', 'postal_code',
            'phone', 'email',
        )
        widgets = {
            'city': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-office'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-7'

        self.helper.layout = Layout(
            Fieldset(
                _('Office Form'),
                Field(
                    'name',
                    'code',
                    'address',
                    'province',
                    'city',
                    'postal_code',
                    'phone',
                    'email',
                    template='inspinia/field_w_sep.html'
                ),
                template='inspinia/layout/fieldset_ibox.html'
            ),
            Div(
                Div(
                    Submit('save', _('Save')),
                    css_class='ibox-content text-right',
                ),
                css_class='ibox float-e-margins',
            )
        )
