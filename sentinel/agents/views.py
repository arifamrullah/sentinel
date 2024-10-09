import os

from dal import autocomplete

from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, DetailView

from braces.views import StaffuserRequiredMixin
from formtools.wizard.views import SessionWizardView

from sentinel.investors.forms import InvestorForm, DepositForm
from .forms import AgentForm, PreviewAgentForm
from .models import Agent


templates = {
    'agent': 'agents/agent_register.html',
    'investor': 'agents/agent_register.html',
    'deposit': 'agents/agent_register.html',
    'preview': 'agents/preview.html'
}


def is_agent_fc(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('agent') or {}
    return cleaned_data.get('position', '') == Agent.POSITION_CHOICES.finconsultant


class AgentRegistrationWizardView(StaffuserRequiredMixin, SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_files/'))

    form_list = [
        ('agent', AgentForm),
        ('investor', InvestorForm),
        ('deposit', DepositForm),
        ('preview', PreviewAgentForm),
    ]

    condition_dict = {
        'investor': is_agent_fc,
        'deposit': is_agent_fc,
        'preview': is_agent_fc,
    }

    def get_template_names(self):

        return [templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(AgentRegistrationWizardView, self).get_context_data(form=form, **kwargs)

        if self.steps.current == 'preview':
            data_from_step_agent = self.get_cleaned_data_for_step('agent')
            data_from_step_investor = self.get_cleaned_data_for_step('investor')
            data_from_step_deposit = self.get_cleaned_data_for_step('deposit')
            context.update({'data_from_step_agent': data_from_step_agent,
                            'data_from_step_investor': data_from_step_investor,
                            'data_from_step_deposit': data_from_step_deposit})

        return context

    def done(self, form_list, **kwargs):
        agent = None
        investor = None

        for i, form in enumerate(form_list):
            if i == 0:
                obj = form.save()
                agent = obj
            elif i == 1:
                obj = form.save(commit=False)
                obj.financial_consultant = agent
                obj.save()
                investor = obj
            elif i == 2:
                obj = form.save(commit=False)
                obj.investor = investor
                obj.save()
            else:
                form.save()

        return redirect('agents:list')


class AgentListView(StaffuserRequiredMixin, ListView):
    model = Agent
    template_name = 'agents/agent_list.html'
    context_object_name = 'agent_list'
    ordering = ('-created',)
    paginate_by = 10


class AgentDetailView(StaffuserRequiredMixin, DetailView):
    model = Agent
    template_name = 'agents/agent_detail.html'


class RecruiterAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Agent.objects.none()

        qs = Agent.objects.all()

        if self.q:
            qs = qs.filter(code__istartswith=self.q) | qs.filter(full_name__icontains=self.q)

        return qs

    def get_result_label(self, item):

        return item.code+" - "+item.full_name
