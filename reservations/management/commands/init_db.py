from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from reservations.models import MealOption


class Command(BaseCommand):
    help = "Create default admin user if it does not exist."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_user(
                username="admin",
                password="password",
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS("Default admin user created."))
        else:
            self.stdout.write("Admin user already exists.")

        alternatives = [
            ("🥩 Steak haché", 50),
            ("🍳 Omelette", 60),
        ]
        for name, order in alternatives:
            MealOption.objects.update_or_create(
                name=name,
                defaults={"is_active": True, "order": order},
            )

        self.stdout.write(self.style.SUCCESS("Meal alternatives ensured."))
