from django.conf.urls import url
from sentinel.utils import views as utils_views
from . import views as core_views


urlpatterns = [
    url(r'^offices/create/cities/$', utils_views.GetCityProvince, name='cities'),
    url(r'^offices/create/$', core_views.OfficeCreateView.as_view(), name='office_create'),
    url(r'^offices/$', core_views.OfficeListView.as_view(), name='office_list'),
]
