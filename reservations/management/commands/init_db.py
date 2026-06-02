from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from reservations.models import MealOption

DEFAULT_ADMIN_USERNAME = "Z999999"
DEFAULT_ADMIN_PASSWORD = "password"


class Command(BaseCommand):
    help = "Create default admin user if it does not exist."

    def handle(self, *args, **options):
        if not User.objects.filter(username=DEFAULT_ADMIN_USERNAME).exists():
            User.objects.create_user(
                username=DEFAULT_ADMIN_USERNAME,
                password=DEFAULT_ADMIN_PASSWORD,
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS("Default admin user created."))
        else:
            self.stdout.write("Default admin user already exists.")

        alternatives = [
            ("🥗 Plat du jour", 10),
            ("🐟 Poisson", 20),
            ("🥩 Steak haché", 30),
            ("🍳 Œufs brouillés", 40),
            ("🍝 Pâtes", 50),
        ]
        for name, order in alternatives:
            MealOption.objects.update_or_create(
                name=name,
                defaults={"is_active": True, "order": order},
            )

        self.stdout.write(self.style.SUCCESS("Meal alternatives ensured."))
