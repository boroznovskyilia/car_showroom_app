# Generated by Django 4.2.7 on 2023-11-13 12:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producer', '0002_alter_producer_date_of_latest_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producer',
            name='date_of_creat',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 13, 15, 10, 12, 343295)),
        ),
        migrations.AlterField(
            model_name='producer',
            name='date_of_latest_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 13, 15, 10, 12, 343295)),
        ),
    ]
