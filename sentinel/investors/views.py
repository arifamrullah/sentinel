import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from braces.views import StaffuserRequiredMixin
from dal import autocomplete
from dateutil.relativedelta import relativedelta
from formtools.wizard.views import SessionWizardView

from sentinel.agents.models import Agent
from .forms import DepositForm, InvestorAgentForm, PreviewInvestorForm, DepositInvestorForm, WithdrawalForm
from .models import Investor, Deposit, Withdrawal


templates = {
    'investor': 'investors/investor_register.html',
    'deposit': 'investors/investor_register.html',
    'preview': 'investors/preview.html'
}


class InvestorRegistrationForm(StaffuserRequiredMixin, SessionWizardView):

    form_list = [
        ('investor', InvestorAgentForm),
        ('deposit', DepositForm),
        ('preview', PreviewInvestorForm),
    ]

    condition_dict = {
        'preview': True,
    }

    def get_template_names(self):

        return [templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(InvestorRegistrationForm, self).get_context_data(form=form, **kwargs)

        if self.steps.current == 'preview':
            data_from_step_investor = self.get_cleaned_data_for_step('investor')
            data_from_step_deposit = self.get_cleaned_data_for_step('deposit')
            context.update({'data_from_step_investor': data_from_step_investor,
                            'data_from_step_deposit': data_from_step_deposit})

        return context

    def done(self, form_list, **kwargs):
        investor = None
        for i, form in enumerate(form_list):
            if i == 0:
                investor = form.save()
            elif i == 1:
                obj = form.save(commit=False)
                obj.investor = investor
                obj.save()
            else:
                form.save()

        return redirect('investors:list')


class InvestorListView(StaffuserRequiredMixin, ListView):
    model = Investor
    template_name = 'investors/investor_list.html'
    context_object_name = 'investor_list'
    ordering = ('-created',)
    paginate_by = 10


class InvestorDetailView(StaffuserRequiredMixin, DetailView):
    model = Investor
    template_name = 'investors/investor_detail.html'


class FinancialConsultAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Agent.objects.none()

        qs = Agent.objects.all()

        if self.q:
            qs = qs.filter(code__istartswith=self.q) | qs.filter(full_name__icontains=self.q)

        return qs

    def get_result_label(self, item):

        return item.code+" - "+item.full_name


class DepositListView(StaffuserRequiredMixin, ListView):
    model = Deposit
    template_name = 'investors/deposit_list.html'
    context_object_name = 'deposit_list'
    ordering = ('-created',)
    paginate_by = 10


class DepositCreateView(StaffuserRequiredMixin, CreateView):
    model = Deposit
    form_class = DepositInvestorForm
    template_name = 'investors/deposit_create.html'
    success_url = reverse_lazy('transactions:deposit_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj_investor = Investor.objects.get(pk=obj.investor.id)
        obj_investor.tax_id_no = form.cleaned_data['npwp']
        obj_investor.save()

        return super(DepositCreateView, self).form_valid(form)


class DepositInvestorDetailView(StaffuserRequiredMixin, DetailView):
    model = Investor
    template_name = 'investors/deposit_investor_detail.html'


class WithdrawalListView(StaffuserRequiredMixin, ListView):
    model = Withdrawal
    template_name = 'investors/withdrawal_list.html'
    context_object_name = 'withdrawal_list'
    ordering = ('-created',)
    paginate_by = 10


class WithdrawalCreateView(StaffuserRequiredMixin, CreateView):
    model = Withdrawal
    form_class = WithdrawalForm
    template_name = 'investors/withdrawal_create.html'
    success_url = reverse_lazy('transactions:withdrawal_list')


class InvestorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Investor.objects.none()

        qs = Investor.objects.all()

        if self.q:

            qs = qs.filter(name__icontains=self.q) | qs.filter(date_of_birth__istartswith=self.q)

        return qs

    def get_result_label(self, item):

        date_of_birth = item.date_of_birth
        if(date_of_birth is not None):
            date_of_birth = item.date_of_birth.strftime('%m/%d/%Y')

        return str(date_of_birth)+" - ("+item.investor_type+")"+" -- "+item.name


class DepositAutocomplete(StaffuserRequiredMixin, autocomplete.Select2QuerySetView):

    def get_queryset(self):

        withdrawals = Withdrawal.objects.filter(id__isnull=False)
        deposit_id = []

        if (withdrawals):
            for withdrawal in withdrawals:
                deposit_id.append(withdrawal.deposit_id)

        qs = Deposit.objects.all().exclude(id__in=deposit_id)

        if self.q:
            qs = qs.filter(form_no__icontains=self.q) | qs.filter(investor__name__icontains=self.q)

        return qs

    def get_result_label(self, item):
        return item.form_no+" - "+str(item.investor)


def GetInvestor(request):

    if request.is_ajax():
        q = request.GET.get('term', '')

        investor = Investor.objects.get(id=q)
        results = []
        investor_json = {}
        investor_json['investor_type'] = investor.investor_type
        investor_json['tax_id_no'] = investor.tax_id_no
        results.append(investor_json)

        data = json.dumps(results)
    else:
        data = 'fail'


def GetDeposit(request):
    if request.is_ajax():
        q = request.GET.get('deposit_id', '')

        deposits = Deposit.objects.filter(id=q)
        results = []
        for deposit in deposits:
            deposit_json = {}
            deposit_json['amount'] = '{:,}'.format(deposit.amount).replace('.00', '').replace(',', '.')
            deposit_json['withdrawal_date'] = deposit.transaction_date + relativedelta(months=int(deposit.invest_tenor))
            deposit_json['invest_tenor'] = deposit.invest_tenor
            deposit_json['invest_return'] = deposit.invest_return
            deposit_json['bank_acc_name'] = deposit.bank_acc_name
            deposit_json['bank_name'] = deposit.bank_name
            deposit_json['bank_acc_no'] = deposit.bank_acc_no
            results.append(deposit_json)

        data = json.dumps(results, cls=DjangoJSONEncoder)
    else:
        data = 'none'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
