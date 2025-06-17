from django.contrib import admin
from .models import UserSubscription, Payment, ResumeOptimization

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'subscription_date', 'expiration_date')
    search_fields = ('user__username', 'plan')
    list_filter = ('plan',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'status', 'created_at')
    search_fields = ('user__username', 'stripe_payment_intent')
    list_filter = ('status', 'currency')

@admin.register(ResumeOptimization)
class ResumeOptimizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'company_name', 'match_score', 'plan_used', 'created_at')
    search_fields = ('user__username', 'job_title', 'company_name')
    list_filter = ('plan_used',)
