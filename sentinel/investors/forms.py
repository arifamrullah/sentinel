from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, Field, HTML
from crispy_forms.bootstrap import AppendedText, PrependedText
from dal import autocomplete

from sentinel.utils.models import Province, Confirmation
from .models import Investor, Deposit, Withdrawal


class PreviewInvestorForm(forms.ModelForm):

    class Meta:
        model = Confirmation
        fields = (
            'confirm',
        )

    def __init__(self, *args, **kwargs):
        super(PreviewInvestorForm, self).__init__(*args, **kwargs)

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
                    css_class='ibox-content text-right',
                ),
                css_class='ibox float-e-margins'
            )
        )


class InvestorForm(forms.ModelForm):

    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select())

    class Meta:
        model = Investor
        fields = (
            'investor_type', 'name', 'pic_corporate', 'pic_position',
            'national_id_card_no', 'date_of_birth',
            'address', 'province', 'city', 'postal_code',
            'phone', 'mobile1', 'mobile2', 'email', 'bank_acc_name',
            'bank_name', 'bank_branch', 'bank_acc_no', 'tax_id_no',
        )
        widgets = {
            'investor_type': forms.RadioSelect(),
            'date_of_birth': forms.TextInput(attrs={'class': 'datepicker_birth'}),
            'name': forms.TextInput(attrs={'class': 'investor_name'}),
            'city': forms.Select(),
            'pic_corporate': forms.TextInput(attrs={'class': 'val_pic_corporate'}),
            'pic_position': forms.TextInput(attrs={'class': 'val_pic_position'}),
            'bank_acc_name': forms.TextInput(attrs={'class': 'investor_bank_acc_name'}),
            'bank_name': forms.TextInput(attrs={'class': 'investor_bank_name'}),
            'bank_acc_no': forms.TextInput(attrs={'class': 'investor_bank_acc_no'}),
        }

    def clean(self):
        cleaned_data = super(InvestorForm, self).clean()

        error_dict = {}

        investor_type = self.cleaned_data['investor_type']
        pic_corporate = self.cleaned_data['pic_corporate']
        pic_position = self.cleaned_data['pic_position']
        tax_id_no = self.cleaned_data['tax_id_no']
        date_of_birth = self.cleaned_data['date_of_birth']

        self.fields['pic_corporate'].required = False
        self.fields['pic_position'].required = False
        self.fields['tax_id_no'].required = False
        self.fields['date_of_birth'].required = False

        if investor_type == "individual":

            self.fields['date_of_birth'].required = True

            if date_of_birth is None:
                error_dict['date_of_birth'] = ValidationError(_('This field is required'), code='required')

        if investor_type == "corporate":

            self.fields['pic_corporate'].required = True
            self.fields['pic_position'].required = True
            self.fields['tax_id_no'].required = True

            if pic_corporate == '':
                error_dict['pic_corporate'] = ValidationError(_('This field is required'), code='required')
            if pic_position == '':
                error_dict['pic_position'] = ValidationError(_('This field is required'), code='required')
            if tax_id_no == '':
                error_dict['tax_id_no'] = ValidationError(_('This field is required'), code='required')

        if error_dict:
            raise ValidationError(error_dict)

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(InvestorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'form-investor'
        self.helper.form_method = 'post'

        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-7'

        self.helper.layout = Layout(
            Fieldset(
                _('Personal Information'),
                Field(
                    'investor_type',
                    'name',
                    Div(
                        Field('pic_corporate', template='inspinia/field_w_sep.html'),
                        style="display:none;", css_class="div_pic"
                    ),
                    Div(
                        Field('pic_position', template='inspinia/field_w_sep.html'),
                        style="display:none;", css_class="div_pic_position"
                    ),
                    'national_id_card_no',
                    'date_of_birth',
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
            Div(
                Div(
                    Submit('continue', _('Continue'), css_class="submit-investor"),
                    css_class='ibox-content text-right',
                ),
                css_class='ibox float-e-margins',
            )
        )


class InvestorAgentForm(InvestorForm):

    class Meta(InvestorForm.Meta):
        fields = InvestorForm.Meta.fields + ('financial_consultant',)
        widgets = InvestorForm.Meta.widgets.copy()
        widgets.update({
            'financial_consultant': autocomplete.Select2(
                url='investors:autofinconsult',
                attrs={
                    'data-minimum-input-length': 3,
                }
            ),
        })

    def __init__(self, *args, **kwargs):
        super(InvestorAgentForm, self).__init__(*args, **kwargs)
        self.helper.layout[0].insert(0, Field('financial_consultant', template='inspinia/field_w_sep.html'))


class DepositForm(forms.ModelForm):

    class Meta:
        model = Deposit
        fields = (
            'form_no', 'deposit_type',
            'amount',
            'transaction_type', 'bank_acc_name', 'bank_name', 'bank_acc_no', 'transaction_date',
            'invest_tenor', 'invest_return', 'product_type'
        )
        widgets = {
            'deposit_type': forms.RadioSelect(attrs={'class': 'deposit_type'}),
            'amount': forms.TextInput(attrs={'class': 'deposit_value'}),
            'transaction_type': forms.RadioSelect(),
            'transaction_date': forms.TextInput(attrs={'class': 'datepicker_depositdate'}),
            'bank_acc_name': forms.TextInput(attrs={'class': 'deposit_bank_acc_name'}),
            'bank_name': forms.TextInput(attrs={'class': 'deposit_bank_name'}),
            'bank_acc_no': forms.TextInput(attrs={'class': 'deposit_bank_acc_no'}),
            'invest_tenor': forms.RadioSelect(),
            'invest_return': forms.TextInput(attrs={'class': 'return_value'}),
            'product_type': forms.RadioSelect(),
        }

    def clean_form_no(self):
        form_no = self.cleaned_data['form_no']

        is_form_no_exist = Deposit.objects.filter(form_no=form_no).exists()
        if is_form_no_exist:
            raise forms.ValidationError("formulir no. is already exist")

        return form_no

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if amount == 0:
            raise forms.ValidationError("amount can not 0 value")

        return amount

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-7'

        self.helper.layout = Layout(
            Fieldset(
                _('Deposit Form'),
                Field(
                    'form_no',
                    'deposit_type',
                    Div(
                        Field(
                            PrependedText('amount', 'Rp.'),
                        ),
                        HTML('<div class="hr-line-dashed"></div>'),
                    ),
                    'transaction_type',
                    'bank_acc_name',
                    'bank_name',
                    'bank_acc_no',
                    'transaction_date',
                    'invest_tenor',
                    AppendedText('invest_return', '%p.a', active=True),
                    template='inspinia/field_w_sep.html'
                ),
                template='inspinia/layout/fieldset_ibox.html'
            ),
            Div(
                Div(
                    Field(
                        'product_type',
                    ),
                    css_class='ibox-content'
                ),
                Div(
                    Submit('save', _('Save'), css_class="submit-deposit"),
                    css_class='ibox-content text-right',
                ),
                css_class='ibox float-e-margins',
            )
        )


class DepositInvestorForm(DepositForm):

    npwp = forms.CharField(max_length=20, required=False, label="NPWP", widget=forms.TextInput(attrs={'class': 'npwp_investor'}))

    class Meta(DepositForm.Meta):
        fields = DepositForm.Meta.fields + ('investor',)
        widgets = DepositForm.Meta.widgets.copy()
        widgets.update({
            'investor': autocomplete.Select2(
                url='transactions:autoinvestor',
                attrs={
                    'data-minimum-input-length': 3,
                    'class': 'investor-choose',
                }
            ),
        })

    def clean(self):

        cleaned_data = super(DepositForm, self).clean()

        deposit_type = self.cleaned_data['deposit_type']
        investor = cleaned_data.get('investor')
        npwp = cleaned_data.get('npwp')

        self.fields['npwp'].required = False

        error_dict = {}

        if (investor):

            is_investor_exist = Investor.objects.filter(id=investor.id).exists()

            if is_investor_exist:
                get_investor = Investor.objects.get(id=investor.id)
                investor_type = get_investor.investor_type

                if investor_type == 'corporate':
                    self.fields['npwp'].required = True

                    if deposit_type == 'netto':
                        error_dict['deposit_type'] = ValidationError(_('deposit must be gross'), code='invalid')

                    if npwp == '':
                        error_dict['npwp'] = ValidationError(_('This field is required.'), code='invalid')

        if error_dict:
            raise ValidationError(error_dict)

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(DepositInvestorForm, self).__init__(*args, **kwargs)
        self.helper.layout[0].insert(0, Field(
            Div(
                'investor',
                HTML('<div id="details-investor" class="form-group"><div class="hr-line-dashed"></div><label for="id_npwp" class="control-label col-md-3">Investor Type</label><div class="col-md-7 data-investor-type"></div></div>'),
                HTML('<div class="hr-line-dashed"></div>'),
            )
        ))

        self.helper.layout[0].insert(1, Field(
            'npwp',
            template='inspinia/field_w_sep.html'
        ))


class WithdrawalForm(forms.ModelForm):

    class Meta:
        model = Withdrawal
        fields = (
            'form_no', 'deposit', 'amount', 'withdrawal_date',
            'notes', 'bank_acc_name', 'bank_name', 'bank_acc_no'
        )
        widgets = {
            'deposit': autocomplete.Select2(
                url='transactions:deposit_autocomplete',
                attrs={'class': 'deposit', 'data-minimum-input-length': 3},
            ),
            'form_no': forms.TextInput(attrs={'class': 'form_no'}),
            'withdrawal_date': forms.TextInput(attrs={'class': 'withdrawal_date datepicker_withdrawaldate'}),
            'amount': forms.TextInput(attrs={'class': 'withdrawal_amount'}),
            'bank_acc_name': forms.TextInput(attrs={'class': 'bank_acc_name'}),
            'bank_name': forms.TextInput(attrs={'class': 'bank_name'}),
            'bank_acc_no': forms.TextInput(attrs={'class': 'bank_acc_no'}),
        }

    def __init__(self, *args, **kwargs):
        super(WithdrawalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'form-deposit'
        self.helper.form_method = 'post'
        self.helper.include_media = False

        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-7'

        self.helper.layout = Layout(
            Fieldset(
                'Withdrawal Transaction',
                'form_no',
                'deposit',
                Div(
                    Field(
                        PrependedText('amount', 'Rp'),
                    ),
                    HTML('<div class="hr-line-dashed"></div>'),
                ),
                'withdrawal_date',
                'notes',
                template='inspinia/layout/fieldset_ibox.html'
            ),
            Fieldset(
                'Bank Information',
                'bank_acc_name',
                'bank_name',
                'bank_acc_no',
                template='inspinia/layout/fieldset_ibox.html'
            ),
            Div(
                Div(
                    Submit('save', _('Save'), css_class='submit-withdrawal'),
                    css_class='ibox-content text-center',
                ),
                css_class='ibox float-e-margins',
            )
        )
