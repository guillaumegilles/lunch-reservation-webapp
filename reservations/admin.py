from django.contrib import admin

from .models import DailyMenu, Lunch, MealOption


@admin.register(MealOption)
class MealOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "order")
    list_editable = ("is_active", "order")
    ordering = ("order", "name")


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_display = ("date", "menu")
    ordering = ("date",)
    date_hierarchy = "date"


@admin.register(Lunch)
class LunchAdmin(admin.ModelAdmin):
    list_display = ("user", "lunch_date", "lunch_choice")
    list_filter = ("lunch_date", "user")
    search_fields = ("user__username", "lunch_choice")
