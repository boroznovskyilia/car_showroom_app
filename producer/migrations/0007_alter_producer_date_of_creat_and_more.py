# Generated by Django 4.2.7 on 2023-11-15 12:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producer', '0006_alter_producer_date_of_creat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producer',
            name='date_of_creat',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 15, 15, 36, 15, 249668)),
        ),
        migrations.AlterField(
            model_name='producer',
            name='date_of_latest_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 15, 15, 36, 15, 249668)),
        ),
    ]