from django.contrib import admin

from .models import Investor, Deposit


class InvestorAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'investor_type', 'national_id_card_no',
        'phone', 'mobile1', 'mobile2', 'created', 'modified',
    )


class DepositAdmin(admin.ModelAdmin):
    list_display = (
        'deposit_type', 'amount', 'transaction_type', 'bank_acc_name', 'bank_name', 'bank_acc_no', 'transaction_date',
        'invest_tenor', 'invest_return', 'created'
    )


admin.site.register(Investor, InvestorAdmin)
admin.site.register(Deposit, DepositAdmin)
