from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^cities/$', views.GetCityProvince, name='cities'),
]
