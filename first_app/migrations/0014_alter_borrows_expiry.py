# Generated by Django 4.2 on 2023-07-30 14:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("first_app", "0013_alter_borrows_expiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrows",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 7, 30, 15, 25, 12, 186831, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]