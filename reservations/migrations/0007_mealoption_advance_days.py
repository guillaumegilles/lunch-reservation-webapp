from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0006_mealrating"),
    ]

    operations = [
        migrations.AddField(
            model_name="mealoption",
            name="advance_days",
            field=models.PositiveSmallIntegerField(default=7),
        ),
    ]
