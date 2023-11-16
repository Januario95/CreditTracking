from django.contrib import admin

from .models import (
    PaymentPlan, Client, Warranty
)


@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'estimated_value')

@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'interest_paid', 'base_amount_paid',
                    'already_paid_interest', 'already_paid_base_amount',
                    'date_paid')
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'job_title',
                    'phone_number2', 'phone_number', 'company', 'amount_requested',
                    'remaining_amount', 'interest_rate', 'months_to_repay',
                    'starting_month', 'id_document', 'contract')