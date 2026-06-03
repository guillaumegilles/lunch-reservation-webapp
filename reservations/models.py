from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MealOption(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class DailyMenu(models.Model):
    date = models.DateField(unique=True)
    menu = models.CharField(max_length=200)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.date} - {self.menu}"


class Lunch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lunch_date = models.DateField()
    lunch_choice = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ("user", "lunch_date")
        ordering = ["user__username", "lunch_date"]

    def __str__(self):
        return f"{self.user.username} - {self.lunch_date} - {self.lunch_choice}"


class MealRating(models.Model):
    lunch = models.OneToOneField(Lunch, on_delete=models.CASCADE, related_name="meal_rating")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.lunch.user.username} - {self.lunch.lunch_date} - {self.rating}/5"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    badge_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.badge_number}"


class Suggestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
