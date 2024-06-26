# Generated by Django 4.2.3 on 2023-07-13 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schedules", "0009_alter_farmerpowerrequirement_transfer_source_pump"),
    ]

    operations = [
        migrations.AlterField(
            model_name="farmerpowerrequirement",
            name="transfer_slot_duriation",
            field=models.CharField(
                choices=[
                    ("full_day", "Full day"),
                    ("half_day", "Half day"),
                    ("quarter_day", "Quarter of the day"),
                ],
                max_length=15,
                null=True,
            ),
        ),
    ]
