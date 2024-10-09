from dal import autocomplete

from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Div, Field

from sentinel.agents.models import Agent
from sentinel.utils.models import Province, Confirmation


class PreviewAgentForm(forms.ModelForm):

    class Meta:
        model = Confirmation
        fields = (
            'confirm',
        )

    def __init__(self, *args, **kwargs):
        super(PreviewAgentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div(
                    'confirm',
                    css_class='text-left row-layout-preview',
                ),
                Div(
                    Submit('submit', _('Confirm & Save')),
                    css_class='text-left',
                ),
                css_class='ibox float-e-margins'
            )
        )


class AgentForm(forms.ModelForm):

    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select())

    class Meta:
        model = Agent
        fields = (
            'full_name', 'national_id_card_no', 'place_of_birth', 'date_of_birth', 'gender',
            'address', 'province', 'city', 'postal_code', 'phone', 'mobile1', 'mobile2',
            'email', 'bank_acc_name', 'bank_name', 'bank_branch',  'bank_acc_no',
            'tax_id_no', 'position', 'office_location', 'recruiter', 'photo'
        )
        widgets = {
            'national_id_card_no': forms.TextInput(attrs={'type': 'number'}),
            'gender': forms.RadioSelect(),
            'position': forms.RadioSelect(),
            'date_of_birth': forms.TextInput(attrs={'class': 'datepicker_birth'}),
            'mobile1': forms.TextInput(attrs={'type': 'number'}),
            'mobile2': forms.TextInput(attrs={'type': 'number'}),
            'city': forms.Select(),
            'office_location': forms.Select(),
            'recruiter': autocomplete.Select2(
                url='agents:autorecruiter',
                attrs={'data-minimum-input-length': 3}
            ),
        }

    def clean_recruiter(self):
        data_recruiter = self.cleaned_data['recruiter']

        count = Agent.objects.count()
        if count >= 1 and not data_recruiter:
            raise forms.ValidationError("recruiter is mandatory")

        return data_recruiter

    def clean_email(self):
        data_email = self.cleaned_data['email']

        is_email_exist = Agent.objects.filter(email=data_email).exists()
        if is_email_exist:
            raise forms.ValidationError("email is already exist")

        return data_email

    def clean_national_id_card_no(self):
        data_cardid = self.cleaned_data['national_id_card_no']

        is_cardid_exist = Agent.objects.filter(national_id_card_no=data_cardid).exists()
        if is_cardid_exist:
            raise forms.ValidationError("national id card no. is already exist")

        return data_cardid

    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-6'

        self.fields['office_location'].label_from_instance = lambda obj: "%s - %s" % (obj.code, obj.name)

        self.helper.layout = Layout(
            Fieldset(
                _('Personal Information'),
                Field(
                    'full_name',
                    'national_id_card_no',
                    'place_of_birth',
                    'date_of_birth',
                    'gender',
                    'address',
                    'province',
                    'city',
                    'postal_code',
                    'phone',
                    'mobile1',
                    'mobile2',
                    'email',
                    template='inspinia/field_w_sep.html'
                ),
                template='inspinia/layout/fieldset_ibox.html'
            ),
            Fieldset(
                _('Bank Information'),
                Field(
                    'bank_acc_name',
                    'bank_name',
                    'bank_branch',
                    'bank_acc_no',
                    'tax_id_no',
                    template='inspinia/field_w_sep.html'
                ),
                template='inspinia/layout/fieldset_ibox.html'
            ),
            Fieldset(
                _('Agent Information'),
                Field(
                    'position',
                    'office_location',
                    'recruiter',
                    template='inspinia/field_w_sep.html'
                ),
                Field(
                    'photo',
                    HTML('<div class="form-group"><div class="col-md-3"></div><div class="col-md-6 style-show"><img id="show-image" src="#" alt="" /></div></div>'),
                ),
                template='inspinia/layout/fieldset_ibox.html'
            ),
            Div(
                Div(
                    HTML('<a class="btn btn-default" href="{}">{}</a> '.format(reverse('agents:list'), _('Cancel'))),
                    Submit('continue', _('Continue')),
                    css_class='ibox-content text-right',
                ),
                css_class='ibox float-e-margins',
            )
        )
