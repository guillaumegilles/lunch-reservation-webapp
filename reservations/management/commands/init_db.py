from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


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
