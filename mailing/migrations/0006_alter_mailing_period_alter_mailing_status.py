# Generated by Django 5.1.1 on 2024-09-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0005_alter_mailing_first_send_date_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="period",
            field=models.IntegerField(
                choices=[
                    (60, "Раз в минуту"),
                    (300, "Раз в 5 минут"),
                    (600, "Раз в 10 минут"),
                ],
                default=60,
                verbose_name="периодичность отправки",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "Создана"),
                    (2, "Запущена"),
                    (3, "Отменена"),
                    (4, "Завершена"),
                ],
                default=0,
                verbose_name="статус рассылки",
            ),
        ),
    ]
