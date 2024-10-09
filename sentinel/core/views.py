from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from braces.views import StaffuserRequiredMixin

from .forms import OfficeForm
from .models import Office


class OfficeListView(StaffuserRequiredMixin, ListView):
    model = Office
    template_name = 'settings/office_list.html'
    context_object_name = 'office_list'
    ordering = ('-created',)
    paginate_by = 10


class OfficeCreateView(StaffuserRequiredMixin, CreateView):
    model = Office
    form_class = OfficeForm
    template_name = 'settings/office_create.html'
    success_url = reverse_lazy('settings:office_list')
