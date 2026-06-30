from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import DailyMenu, Lunch, MealOption, MealRating, Suggestion, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdminWithProfile(UserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdminWithProfile)


@admin.register(MealOption)
class MealOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "advance_days", "order")
    list_editable = ("is_active", "advance_days", "order")
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


@admin.register(MealRating)
class MealRatingAdmin(admin.ModelAdmin):
    list_display = ("lunch", "rating", "created_at", "updated_at")
    list_filter = ("rating", "created_at", "updated_at")
    search_fields = ("lunch__user__username", "lunch__lunch_choice")


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ("user", "text_short", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("user__username", "text")
    list_editable = ("is_read",)
    readonly_fields = ("created_at", "user")
    ordering = ("-created_at",)
    
    def text_short(self, obj):
        """Display truncated suggestion text in list view."""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_short.short_description = "Suggestion"
