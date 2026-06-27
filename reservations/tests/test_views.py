import json
from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core import mail
from django.db import ProgrammingError
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localdate

from reservations.models import DailyMenu, Lunch, MealOption, MealRating, Suggestion, UserProfile


class AuthFlowTests(TestCase):
    def test_register_creates_user_and_redirects(self):
        response = self.client.post(
            reverse("register"),
            {
                "identifier": "K589479",
                "badge_number": "123456",
                "last_name": "Durand",
                "first_name": "Alice",
                "password": "A12345xy",
                "confirm_password": "A12345xy",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="K589479", first_name="Alice", last_name="Durand").exists())

        created_user = User.objects.get(username="K589479")
        self.assertTrue(created_user.check_password("A12345xy"))
        self.assertTrue(UserProfile.objects.filter(user__username="K589479", badge_number="123456").exists())

    def test_register_rejects_invalid_identifier_format(self):
        response = self.client.post(
            reverse("register"),
            {
                "identifier": "5894799",
                "badge_number": "123456",
                "last_name": "Durand",
                "first_name": "Alice",
                "password": "A12345xy",
                "confirm_password": "A12345xy",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(last_name="Durand", first_name="Alice").exists())

    def test_register_rejects_weak_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "identifier": "K589479",
                "badge_number": "123456",
                "last_name": "Durand",
                "first_name": "Alice",
                "password": "12345678",
                "confirm_password": "12345678",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="K589479").exists())

    def test_register_rejects_mismatched_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "identifier": "K589479",
                "badge_number": "123456",
                "last_name": "Durand",
                "first_name": "Alice",
                "password": "A12345xy",
                "confirm_password": "DIFFERENT",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="K589479").exists())

    def test_login_success_redirects_to_calendar(self):
        User.objects.create_user(
            username="K589479",
            last_name="Durand",
            password="12345",
        )

        response = self.client.post(
            reverse("login"),
            {
                "identifier": "k589479",
                "password": "12345",
            },
        )

        self.assertRedirects(response, reverse("calendar"))

    def test_index_redirects_authenticated_user_to_dashboard(self):
        user = User.objects.create_user(username="K589479", password="12345")
        self.client.force_login(user)

        response = self.client.get(reverse("index"))

        self.assertRedirects(response, reverse("dashboard"))

    def test_login_rejects_wrong_identifier_or_badge(self):
        User.objects.create_user(
            username="K589479",
            last_name="Durand",
            password="12345",
        )

        wrong_identifier = self.client.post(
            reverse("login"),
            {
                "identifier": "X123456",
                "password": "12345",
            },
        )
        self.assertEqual(wrong_identifier.status_code, 200)

        wrong_badge = self.client.post(
            reverse("login"),
            {
                "identifier": "K589479",
                "password": "99999",
            },
        )
        self.assertEqual(wrong_badge.status_code, 200)


class CalendarAndLunchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jane", password="secret123")
        MealOption.objects.create(name="Plat du jour", is_active=True)

    def test_calendar_requires_authentication(self):
        response = self.client.get(reverse("calendar"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_save_lunch_for_future_date_creates_or_updates_entry(self):
        self.client.login(username="jane", password="secret123")
        future = date.today() + timedelta(days=8)

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

    def test_calendar_days_are_blank_without_existing_reservation(self):
        self.client.login(username="jane", password="secret123")

        response = self.client.get(reverse("calendar"))

        self.assertEqual(response.status_code, 200)
        days = response.context["days"]
        self.assertTrue(all(day.get("lunch", "") == "" for day in days))

    def test_calendar_options_come_from_meal_option_model(self):
        self.client.login(username="jane", password="secret123")

        response = self.client.get(reverse("calendar"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("options", response.context)
        self.assertEqual(list(response.context["options"]), [{"name": "Plat du jour", "advance_days": 7}])

    def test_calendar_falls_back_when_advance_days_column_is_missing(self):
        self.client.login(username="jane", password="secret123")
        original_values = QuerySet.values

        def values_with_missing_advance_days(queryset, *fields, **expressions):
            if fields == ("name", "advance_days"):
                raise ProgrammingError('column reservations_mealoption.advance_days does not exist')
            return original_values(queryset, *fields, **expressions)

        with patch.object(QuerySet, "values", autospec=True, side_effect=values_with_missing_advance_days):
            response = self.client.get(reverse("calendar"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["options"]), [{"name": "Plat du jour", "advance_days": 7}])

    def test_calendar_prefers_matching_daily_menu_option(self):
        self.client.login(username="jane", password="secret123")
        matching_label = "Poulet rôti aux herbes"
        MealOption.objects.create(name=matching_label, is_active=True, order=1)
        MealOption.objects.create(name="Poisson du jour", is_active=True, order=2)
        future = date.today() + timedelta(days=14)
        DailyMenu.objects.create(date=future, menu=matching_label)

        response = self.client.get(
            reverse("calendar"),
            {"year": future.year, "month": future.month},
        )

        self.assertEqual(response.status_code, 200)
        days = {d["day"]: d for d in response.context["days"]}
        self.assertEqual(days[future.day]["default_option"], matching_label)

    def test_calendar_falls_back_to_first_active_option_when_menu_does_not_match(self):
        self.client.login(username="jane", password="secret123")
        MealOption.objects.create(name="Menu de secours", is_active=True, order=1)
        MealOption.objects.create(name="Poisson du jour", is_active=True, order=2)
        future = date.today() + timedelta(days=14)
        DailyMenu.objects.create(date=future, menu="Menu fantaisie sans correspondance")

        response = self.client.get(
            reverse("calendar"),
            {"year": future.year, "month": future.month},
        )

        self.assertEqual(response.status_code, 200)
        days = {d["day"]: d for d in response.context["days"]}
        self.assertEqual(days[future.day]["default_option"], "Plat du jour")

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

    def test_calendar_exposes_existing_rating_for_past_lunch(self):
        self.client.login(username="jane", password="secret123")
        past = date.today() - timedelta(days=2)
        lunch = Lunch.objects.create(user=self.user, lunch_date=past, lunch_choice="Plat du jour")
        MealRating.objects.create(lunch=lunch, rating=4)

        response = self.client.get(
            reverse("calendar"),
            {"year": past.year, "month": past.month},
        )

        self.assertEqual(response.status_code, 200)
        days = {d["day"]: d for d in response.context["days"]}
        self.assertEqual(days[past.day]["rating"], 4)
        self.assertTrue(days[past.day]["can_rate"])

    def test_calendar_disables_ratings_when_table_is_missing(self):
        self.client.login(username="jane", password="secret123")

        with patch("reservations.views._meal_rating_table_exists", return_value=False):
            response = self.client.get(reverse("calendar"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["ratings_enabled"])

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

    def test_save_lunch_within_7_days_returns_400(self):
        self.client.login(username="jane", password="secret123")
        near = date.today() + timedelta(days=3)

        payload = {
            "day": near.day,
            "month": near.month,
            "year": near.year,
            "lunch": "Plat du jour",
        }
        response = self.client.post(
            reverse("save_lunch"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Lunch.objects.filter(user=self.user, lunch_date=near).exists())

    def test_save_lunch_rejects_invalid_option(self):
        self.client.login(username="jane", password="secret123")
        future = date.today() + timedelta(days=8)

        payload = {
            "day": future.day,
            "month": future.month,
            "year": future.year,
            "lunch": "Steak",
        }
        response = self.client.post(
            reverse("save_lunch"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Lunch.objects.filter(user=self.user, lunch_date=future).exists())

    def test_save_lunch_falls_back_when_advance_days_column_is_missing(self):
        self.client.login(username="jane", password="secret123")
        future = date.today() + timedelta(days=8)
        original_values = QuerySet.values

        def values_with_missing_advance_days(queryset, *fields, **expressions):
            if fields == ("name", "advance_days"):
                raise ProgrammingError('column reservations_mealoption.advance_days does not exist')
            return original_values(queryset, *fields, **expressions)

        with patch.object(QuerySet, "values", autospec=True, side_effect=values_with_missing_advance_days):
            response = self.client.post(
                reverse("save_lunch"),
                data=json.dumps(
                    {
                        "day": future.day,
                        "month": future.month,
                        "year": future.year,
                        "lunch": "Plat du jour",
                    }
                ),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Lunch.objects.filter(user=self.user, lunch_date=future).exists())

    def test_save_lunch_cancellation_deletes_reservation(self):
        self.client.login(username="jane", password="secret123")
        future = date.today() + timedelta(days=8)
        Lunch.objects.create(user=self.user, lunch_date=future, lunch_choice="Plat du jour")

        payload = {
            "day": future.day,
            "month": future.month,
            "year": future.year,
            "lunch": "",
        }
        response = self.client.post(
            reverse("save_lunch"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Lunch.objects.filter(user=self.user, lunch_date=future).exists())

    def test_save_meal_rating_creates_and_overwrites_rating(self):
        self.client.login(username="jane", password="secret123")
        past = date.today() - timedelta(days=2)
        lunch = Lunch.objects.create(user=self.user, lunch_date=past, lunch_choice="Plat du jour")

        response = self.client.post(
            reverse("save_meal_rating"),
            data=json.dumps({"day": past.day, "month": past.month, "year": past.year, "rating": 3}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MealRating.objects.get(lunch=lunch).rating, 3)

        update_response = self.client.post(
            reverse("save_meal_rating"),
            data=json.dumps({"day": past.day, "month": past.month, "year": past.year, "rating": 5}),
            content_type="application/json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(MealRating.objects.get(lunch=lunch).rating, 5)

    def test_save_meal_rating_rejects_today_or_without_reservation(self):
        self.client.login(username="jane", password="secret123")
        today = date.today()

        today_response = self.client.post(
            reverse("save_meal_rating"),
            data=json.dumps({"day": today.day, "month": today.month, "year": today.year, "rating": 4}),
            content_type="application/json",
        )
        self.assertEqual(today_response.status_code, 400)

        past = date.today() - timedelta(days=3)
        missing_response = self.client.post(
            reverse("save_meal_rating"),
            data=json.dumps({"day": past.day, "month": past.month, "year": past.year, "rating": 4}),
            content_type="application/json",
        )
        self.assertEqual(missing_response.status_code, 400)

    def test_save_meal_rating_returns_503_when_table_is_missing(self):
        self.client.login(username="jane", password="secret123")
        past = date.today() - timedelta(days=2)
        Lunch.objects.create(user=self.user, lunch_date=past, lunch_choice="Plat du jour")

        with patch("reservations.views._meal_rating_table_exists", return_value=False):
            response = self.client.post(
                reverse("save_meal_rating"),
                data=json.dumps({"day": past.day, "month": past.month, "year": past.year, "rating": 4}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 503)

    def test_calendar_uses_localdate_not_utc_today(self):
        """can_rate and can_reserve must use the configured timezone (Europe/Paris),
        not the server's UTC clock. We simulate the UTC-vs-Paris boundary by patching
        localdate to return a date one day ahead of date.today()."""
        self.client.login(username="jane", password="secret123")
        # Simulated Paris date is one day ahead of the server's UTC date.
        paris_today = date.today() + timedelta(days=1)
        paris_yesterday = paris_today - timedelta(days=1)
        Lunch.objects.create(user=self.user, lunch_date=paris_yesterday, lunch_choice="Plat du jour")

        with patch("reservations.views.localdate", return_value=paris_today):
            response = self.client.get(
                reverse("calendar"),
                {"year": paris_yesterday.year, "month": paris_yesterday.month},
            )

        self.assertEqual(response.status_code, 200)
        days = {d["day"]: d for d in response.context["days"]}
        day_ctx = days[paris_yesterday.day]
        # paris_yesterday < paris_today → can_rate must be True
        self.assertTrue(day_ctx["can_rate"], "can_rate should be True for paris_yesterday when localdate is paris_today")
        # paris_yesterday is not >= paris_today + 7 days → can_reserve must be False
        self.assertFalse(day_ctx["can_reserve"])

    def test_save_meal_rating_uses_localdate_not_utc_today(self):
        """Rating a past date must use localdate(), not date.today().
        Simulates the midnight boundary: server UTC = yesterday, Paris = today.
        A meal from UTC-yesterday is 'today' in UTC but 'yesterday' in Paris — must be rateable."""
        self.client.login(username="jane", password="secret123")
        utc_yesterday = date.today() - timedelta(days=1)
        paris_today = date.today()
        Lunch.objects.create(user=self.user, lunch_date=utc_yesterday, lunch_choice="Plat du jour")

        # localdate() returns paris_today; utc_yesterday < paris_today → should be rateable
        with patch("reservations.views.localdate", return_value=paris_today):
            response = self.client.post(
                reverse("save_meal_rating"),
                data=json.dumps({"day": utc_yesterday.day, "month": utc_yesterday.month, "year": utc_yesterday.year, "rating": 5}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)

    def test_save_lunch_7_day_guard_uses_localdate(self):
        """The 7-day reservation guard must use localdate() so Paris-timezone users
        get a consistent cutoff regardless of the server's UTC clock."""
        self.client.login(username="jane", password="secret123")
        # Paris date is 1 day ahead of UTC; 8 days from Paris today = 8 days from UTC tomorrow
        paris_today = date.today() + timedelta(days=1)
        target = paris_today + timedelta(days=8)

        with patch("reservations.views.localdate", return_value=paris_today):
            response = self.client.post(
                reverse("save_lunch"),
                data=json.dumps({"day": target.day, "month": target.month, "year": target.year, "lunch": "Plat du jour"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)


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

    def test_admin_summary_shows_average_and_individual_ratings(self):
        self.client.login(username="staff", password="secret123")
        target_date = date.today() - timedelta(days=2)
        lunch_one = Lunch.objects.create(user=self.user, lunch_date=target_date, lunch_choice="Plat du jour")
        MealRating.objects.create(lunch=lunch_one, rating=4)
        second_user = User.objects.create_user(username="user2", password="secret123")
        lunch_two = Lunch.objects.create(user=second_user, lunch_date=target_date, lunch_choice="Poisson")
        MealRating.objects.create(lunch=lunch_two, rating=2)

        response = self.client.get(
            reverse("admin_summary"),
            {"year": target_date.year, "month": target_date.month},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "★ 3.0 / 5")
        self.assertContains(response, "★ 4/5")
        self.assertContains(response, "★ 2/5")


class SuggestionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="K589479",
            first_name="Alice",
            last_name="Durand",
            password="secret123",
        )

    def test_authenticated_user_can_submit_suggestion(self):
        self.client.login(username="K589479", password="secret123")

        response = self.client.post(
            reverse("submit_suggestion"),
            {"text": "Ajouter un rappel sur le dashboard."},
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Suggestion de K589479")
        self.assertIn("Ajouter un rappel sur le dashboard.", mail.outbox[0].body)
        self.assertTrue(Suggestion.objects.filter(user=self.user, text="Ajouter un rappel sur le dashboard.").exists())

    def test_suggestion_requires_authentication(self):
        response = self.client.post(
            reverse("submit_suggestion"),
            {"text": "Test"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
