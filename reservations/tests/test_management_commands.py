from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from reservations.management.commands.init_db import DEFAULT_ADMIN_USERNAME
from reservations.models import MealOption


class InitDbCommandTests(TestCase):
    def test_init_db_creates_default_staff_user(self):
        call_command("init_db")

        admin_user = User.objects.get(username=DEFAULT_ADMIN_USERNAME)

        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.check_password("password"))

    def test_init_db_is_idempotent_for_default_user(self):
        call_command("init_db")
        call_command("init_db")

        self.assertEqual(User.objects.filter(username=DEFAULT_ADMIN_USERNAME).count(), 1)
        self.assertEqual(MealOption.objects.filter(name="🥩 Steak haché").count(), 1)

    def test_init_db_seeds_default_meal_options(self):
        call_command("init_db")

        self.assertGreaterEqual(MealOption.objects.filter(is_active=True).count(), 5)
        self.assertTrue(MealOption.objects.filter(name__startswith="🥗").exists())
        self.assertTrue(MealOption.objects.filter(name__startswith="🐟").exists())
        self.assertTrue(MealOption.objects.filter(name__startswith="🥩").exists())
        self.assertTrue(MealOption.objects.filter(name__startswith="🍳").exists())
        self.assertTrue(MealOption.objects.filter(name__startswith="🍝").exists())

        # Verify idempotency: call init_db twice, count must not grow
        count_after_first = MealOption.objects.count()
        call_command("init_db")
        count_after_second = MealOption.objects.count()
        self.assertEqual(count_after_first, count_after_second)
