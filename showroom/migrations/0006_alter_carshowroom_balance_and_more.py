# Generated by Django 4.2.7 on 2023-11-13 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0005_alter_carshowroom_date_of_creat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carshowroom',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='carshowroom',
            name='date_of_creat',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 13, 15, 11, 32, 360932)),
        ),
        migrations.AlterField(
            model_name='carshowroom',
            name='date_of_latest_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 13, 15, 11, 32, 360932)),
        ),
    ]