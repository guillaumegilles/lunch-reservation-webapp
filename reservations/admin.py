from django.contrib import admin

from .models import Lunch


@admin.register(Lunch)
class LunchAdmin(admin.ModelAdmin):
    list_display = ("user", "lunch_date", "lunch_choice")
    list_filter = ("lunch_date", "user")
    search_fields = ("user__username", "lunch_choice")
