# Generated by Django 4.1 on 2024-06-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_user_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="is_Active"),
        ),
    ]