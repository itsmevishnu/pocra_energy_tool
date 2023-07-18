# Generated by Django 4.2.3 on 2023-07-13 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("schedules", "0006_daynightschedule"),
    ]

    operations = [
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="crop",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="schedules.crop",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="days_for_irrigation",
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="irrigation_start_within",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="is_night_irrigation",
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="is_transfer_from_source",
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="last_irrigation_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="number_of_slots",
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="period_between_irrigation",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="schedule",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="schedules.schedule",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="slot_duration",
            field=models.CharField(
                choices=[
                    ("full_day", "Full day"),
                    ("half_day", "Half day"),
                    ("quarter_day", "Quarter of the day"),
                ],
                default=None,
                max_length=15,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="transfer_slot_duriation",
            field=models.CharField(
                choices=[
                    ("full_day", "Full day"),
                    ("half_day", "Half day"),
                    ("quarter_day", "Quarter of the day"),
                ],
                default=None,
                max_length=15,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="crop",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="crop",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="farmer",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="farmer",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="irrigationmethod",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="irrigationmethod",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="soiltype",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="soiltype",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.CreateModel(
            name="FarmerPumpRelation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "source_type",
                    models.CharField(
                        choices=[
                            ("open_well", "Open well"),
                            ("bore_well", "Bore well"),
                            ("surface_water", "Surface water"),
                            ("other", "Other"),
                        ],
                        max_length=15,
                    ),
                ),
                ("capacity", models.FloatField()),
                ("direct_to_field", models.BooleanField()),
                (
                    "farmer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedules.farmer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="farmerpowerrequirement",
            name="irrigation_pump",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="schedules.farmerpumprelation",
            ),
            preserve_default=False,
        ),
    ]
