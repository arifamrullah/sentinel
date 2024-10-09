from django.conf.urls import url

from sentinel.utils import views as utils_views
from . import views as investors_views


urlpatterns = [
    url(r'^register/cities/$', utils_views.GetCityProvince, name='cities'),
    url(r'^register/autofinconsult/$', investors_views.FinancialConsultAutocomplete.as_view(), name='autofinconsult'),
    url(r'^register/$', investors_views.InvestorRegistrationForm.as_view(), name='register'),
    url(r'^(?P<pk>\d+)/$', investors_views.InvestorDetailView.as_view(), name='detail'),
    url(r'^$', investors_views.InvestorListView.as_view(), name='list'),
]
