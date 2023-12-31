# Generated by Django 4.2 on 2023-07-30 07:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("first_app", "0009_alter_borrows_expiry_reservations"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservations",
            name="is_reserved",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="borrows",
            name="expiry",
            field=models.DateField(
                default=datetime.datetime(2023, 8, 13, 13, 16, 33, 207266)
            ),
        ),
    ]
