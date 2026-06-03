from datetime import date, timedelta

from django.core.management.base import BaseCommand

from reservations.models import DailyMenu


MENU_ROTATION = {
    0: [
        "Salade de lentilles, tomates confites et feta",
        "Bowl de riz noir, avocat et pickles de légumes",
        "Quinoa aux herbes, pois chiches et carottes rôties",
        "Salade de pâtes au pesto, tomates cerises et mozzarella",
        "Velouté de petits pois, croûtons et chèvre frais",
    ],
    1: [
        "Poulet rôti aux herbes, pommes grenaille et haricots verts",
        "Curry doux de légumes au lait de coco",
        "Boeuf mijoté aux carottes et purée maison",
        "Chili sin carne, riz parfumé et maïs grillé",
        "Wok de légumes, nouilles soba et tofu mariné",
    ],
    2: [
        "Quiche épinards-chèvre et salade croquante",
        "Lasagnes de légumes grillés et salade verte",
        "Poulet basquaise, semoule et ratatouille",
        "Gratin de courgettes, quinoa et sauce yaourt aux herbes",
    ],
    3: [
        "Filet de dinde sauce moutarde, riz pilaf et courgettes",
        "Tartiflette légère et salade composée",
        "Tarte tomate-moutarde et salade de saison",
        "Escalope de volaille sauce champignons, purée de patate douce",
    ],
    4: [
        "Menu festif du vendredi: pavé de saumon, risotto citronné et dessert aux fruits rouges",
        "Menu festif du vendredi: dos de colin, millefeuille de légumes et tarte fine",
        "Menu festif du vendredi: rôti de porc aux pruneaux, gratin dauphinois et mousse au chocolat",
        "Menu festif du vendredi: burger maison, potatoes et cheesecake citron",
    ],
}


def _june_2026_workdays():
    current = date(2026, 6, 1)
    end = date(2026, 6, 30)
    while current <= end:
        if current.weekday() < 5:
            yield current
        current += timedelta(days=1)


def _menu_for_workday(workday, weekday_counts):
    weekday = workday.weekday()
    index = weekday_counts[weekday]
    labels = MENU_ROTATION[weekday]
    if index >= len(labels):
        raise RuntimeError("June menu seed data does not cover all working days.")
    weekday_counts[weekday] += 1
    return labels[index]


class Command(BaseCommand):
    help = "Seed varied lunch menus for June 2026."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing June menus instead of leaving them untouched.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        created = 0
        updated = 0
        unchanged = 0

        workdays = list(_june_2026_workdays())
        weekday_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

        for workday in workdays:
            menu_label = _menu_for_workday(workday, weekday_counts)
            menu, is_created = DailyMenu.objects.get_or_create(date=workday, defaults={"menu": menu_label})
            if is_created:
                created += 1
                continue

            if force and menu.menu != menu_label:
                menu.menu = menu_label
                menu.save(update_fields=["menu"])
                updated += 1
            else:
                unchanged += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"June menus seeded: {created} created, {updated} updated, {unchanged} unchanged."
            )
        )
