# Generated by Django 5.1.1 on 2024-09-15 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0003_alter_mailing_last_send_date_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="status",
            field=models.IntegerField(
                choices=[
                    ("COMPLETED", "Завершена"),
                    ("CREATED", "Создана"),
                    ("STARTED", "Запущена"),
                ],
                default=1,
                verbose_name="статус рассылки",
            ),
        ),
    ]
