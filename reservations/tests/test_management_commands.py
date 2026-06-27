from unittest.mock import patch

from django.db import ProgrammingError
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from reservations.management.commands.init_db import DEFAULT_ADMIN_USERNAME
from reservations.models import DailyMenu, MealOption
from datetime import date


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

    def test_init_db_falls_back_when_advance_days_column_is_missing(self):
        def side_effect(*, name, defaults):
            if "advance_days" in defaults:
                raise ProgrammingError("column reservations_mealoption.advance_days does not exist")
            return MealOption(name=name), True

        with patch(
            "reservations.management.commands.init_db.MealOption.objects.update_or_create",
            side_effect=side_effect,
        ):
            call_command("init_db")


class SeedJuneMenusCommandTests(TestCase):
    def test_seed_june_menus_creates_varied_working_day_rows(self):
        call_command("seed_june_menus")

        june_menus = DailyMenu.objects.filter(date__year=2026, date__month=6)
        self.assertEqual(june_menus.count(), 22)
        self.assertGreaterEqual(june_menus.values_list("menu", flat=True).distinct().count(), 6)
        self.assertTrue(all(menu.date.weekday() < 5 for menu in june_menus))
        friday_menus = [menu for menu in june_menus if menu.date.weekday() == 4]
        self.assertTrue(friday_menus)
        self.assertTrue(all("festif" in menu.menu.lower() for menu in friday_menus))

    def test_seed_june_menus_is_idempotent(self):
        call_command("seed_june_menus")
        count_after_first_run = DailyMenu.objects.filter(date__year=2026, date__month=6).count()
        call_command("seed_june_menus")
        count_after_second_run = DailyMenu.objects.filter(date__year=2026, date__month=6).count()

        self.assertEqual(count_after_first_run, count_after_second_run)

    def test_seed_june_menus_force_replaces_existing_rows(self):
        call_command("seed_june_menus")
        target_date = date(2026, 6, 5)
        DailyMenu.objects.filter(date=target_date).update(menu="Menu bricolé")

        call_command("seed_june_menus", force=True)

        self.assertIn("festif", DailyMenu.objects.get(date=target_date).menu.lower())
