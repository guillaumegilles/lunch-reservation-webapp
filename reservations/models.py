from django.conf import settings
from django.db import models


class Lunch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lunch_date = models.DateField()
    lunch_choice = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ("user", "lunch_date")
        ordering = ["user__username", "lunch_date"]

    def __str__(self):
        return f"{self.user.username} - {self.lunch_date} - {self.lunch_choice}"
