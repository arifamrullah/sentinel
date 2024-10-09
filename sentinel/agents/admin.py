from django.contrib import admin

from .models import Agent


class AgentAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'national_id_card_no', 'gender', 'email', 'phone',
        'mobile1', 'mobile2', 'position', 'created', 'modified',
    )


admin.site.register(Agent, AgentAdmin)
