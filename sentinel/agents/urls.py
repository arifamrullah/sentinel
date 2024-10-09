from django.conf.urls import url
from sentinel.agents import views as agents_views
from sentinel.utils import views as utils_views


urlpatterns = [
    url(r'^register/cities/$', utils_views.GetCityProvince, name='cities'),
    url(r'^register/autorecruiter/$', agents_views.RecruiterAutocomplete.as_view(), name='autorecruiter'),
    url(r'^register/$', agents_views.AgentRegistrationWizardView.as_view(), name='register'),
    url(r'^(?P<pk>\d+)/$', agents_views.AgentDetailView.as_view(), name='detail'),
    url(r'^$', agents_views.AgentListView.as_view(), name='list'),
]
