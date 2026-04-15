import json
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from reservations.models import DailyMenu, Lunch


class AuthFlowTests(TestCase):
    def test_register_creates_user_and_redirects(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "alice",
                "password": "secret123",
                "confirm": "secret123",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_register_rejects_mismatched_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "alice",
                "password": "secret123",
                "confirm": "different",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="alice").exists())

    def test_login_success_redirects_to_calendar(self):
        User.objects.create_user(username="bob", password="secret123")

        response = self.client.post(
            reverse("login"),
            {
                "username": "bob",
                "password": "secret123",
            },
        )

        self.assertRedirects(response, reverse("calendar"))


class CalendarAndLunchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jane", password="secret123")

    def test_calendar_requires_authentication(self):
        response = self.client.get(reverse("calendar"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_save_lunch_for_future_date_creates_or_updates_entry(self):
        self.client.login(username="jane", password="secret123")
        future = date.today() + timedelta(days=1)

        payload = {
            "day": future.day,
            "month": future.month,
            "year": future.year,
            "lunch": "Plat du jour",
        }
        response = self.client.post(
            reverse("save_lunch"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        lunch = Lunch.objects.get(user=self.user, lunch_date=future)
        self.assertEqual(lunch.lunch_choice, "Plat du jour")

    def test_calendar_includes_daily_menu_for_each_day(self):
        self.client.login(username="jane", password="secret123")

        response = self.client.get(reverse("calendar"))

        self.assertEqual(response.status_code, 200)
        days = response.context["days"]
        self.assertTrue(len(days) > 0)
        self.assertTrue(all(day.get("menu") for day in days))
        self.assertTrue(all(date(response.context["year"], response.context["month"], day["day"]).weekday() < 5 for day in days))

    def test_db_menu_overrides_default_for_specific_date(self):
        self.client.login(username="jane", password="secret123")
        future = date.today() + timedelta(days=1)
        DailyMenu.objects.create(date=future, menu="🍱 Menu spécial test")

        response = self.client.get(
            reverse("calendar"),
            {"year": future.year, "month": future.month},
        )

        self.assertEqual(response.status_code, 200)
        days = {d["day"]: d for d in response.context["days"]}
        self.assertEqual(days[future.day]["menu"], "🍱 Menu spécial test")

    def test_save_lunch_for_past_date_returns_400(self):
        self.client.login(username="jane", password="secret123")
        past = date.today() - timedelta(days=1)

        payload = {
            "day": past.day,
            "month": past.month,
            "year": past.year,
            "lunch": "Poisson",
        }
        response = self.client.post(
            reverse("save_lunch"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Lunch.objects.filter(user=self.user, lunch_date=past).exists())


class AdminSummaryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="secret123")
        self.staff = User.objects.create_user(
            username="staff",
            password="secret123",
            is_staff=True,
        )

    def test_admin_summary_denied_for_non_staff(self):
        self.client.login(username="user", password="secret123")
        response = self.client.get(reverse("admin_summary"))

        self.assertRedirects(response, reverse("calendar"))

    def test_admin_summary_accessible_for_staff(self):
        self.client.login(username="staff", password="secret123")
        response = self.client.get(reverse("admin_summary"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin.html")

    def test_staff_can_create_weekly_menus(self):
        self.client.login(username="staff", password="secret123")

        payload = {
            "week_start": "2030-01-07",
            "monday_menu": "Lundi menu",
            "tuesday_menu": "Mardi menu",
            "wednesday_menu": "Mercredi menu",
            "thursday_menu": "Jeudi menu",
            "friday_menu": "Vendredi menu",
            "summary_year": "2030",
            "summary_month": "1",
        }
        response = self.client.post(reverse("admin_summary"), payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(DailyMenu.objects.filter(date__year=2030, date__month=1).count(), 5)
        self.assertTrue(DailyMenu.objects.filter(date="2030-01-07", menu="Lundi menu").exists())
        self.assertTrue(DailyMenu.objects.filter(date="2030-01-11", menu="Vendredi menu").exists())
        self.assertFalse(DailyMenu.objects.filter(date="2030-01-12").exists())
        self.assertFalse(DailyMenu.objects.filter(date="2030-01-13").exists())

    def test_staff_weekly_menu_requires_monday(self):
        self.client.login(username="staff", password="secret123")

        payload = {
            "week_start": "2030-01-08",
            "monday_menu": "Lundi menu",
            "tuesday_menu": "Mardi menu",
            "wednesday_menu": "Mercredi menu",
            "thursday_menu": "Jeudi menu",
            "friday_menu": "Vendredi menu",
            "summary_year": "2030",
            "summary_month": "1",
        }
        response = self.client.post(reverse("admin_summary"), payload)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Veuillez choisir un lundi")
        self.assertEqual(DailyMenu.objects.filter(date__year=2030, date__month=1).count(), 0)
