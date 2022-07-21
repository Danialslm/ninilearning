from django.contrib import admin
from .models import Plan, DiscountCode


@admin.register(Plan)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan_time', 'price', 'discounted_price')


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code',)
