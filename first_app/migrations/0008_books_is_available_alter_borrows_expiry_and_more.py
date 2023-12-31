# Generated by Django 4.2 on 2023-07-29 13:59

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("first_app", "0007_alter_borrows_expiry_borrow_requests"),
    ]

    operations = [
        migrations.AddField(
            model_name="books",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="borrows",
            name="expiry",
            field=models.DateField(
                default=datetime.datetime(2023, 8, 12, 19, 59, 26, 327125)
            ),
        ),
        migrations.AlterUniqueTogether(
            name="borrow_requests",
            unique_together={("user", "book")},
        ),
    ]
