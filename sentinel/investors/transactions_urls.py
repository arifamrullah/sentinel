from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^deposits/create/getinvestor/$', views.GetInvestor, name='getinvestor'),
    url(r'^deposits/create/autoinvestor/$', views.InvestorAutocomplete.as_view(), name='autoinvestor'),
    url(r'^deposits/create/$', views.DepositCreateView.as_view(), name='deposit_create'),
    url(r'^deposits/$', views.DepositListView.as_view(), name='deposit_list'),
    url(r'^deposits/(?P<pk>\d+)/$', views.DepositInvestorDetailView.as_view(), name='investor_detail'),

    url(r'^withdrawals/create/$', views.WithdrawalCreateView.as_view(), name='withdrawal_create'),
    url(r'^withdrawals/create/autodeposit/$', views.DepositAutocomplete.as_view(), name='deposit_autocomplete'),
    url(r'^withdrawals/$', views.WithdrawalListView.as_view(), name='withdrawal_list'),
    url(r'^withdrawals/create/get_deposit/$', views.GetDeposit, name='get_deposit'),
]
