# Generated by Django 4.2.7 on 2023-11-17 10:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0013_alter_carshowroom_date_of_creat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carshowroomstock',
            name='date_of_creat',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 13, 37, 56, 626937)),
        ),
        migrations.AddField(
            model_name='carshowroomstock',
            name='date_of_latest_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 13, 37, 56, 626937)),
        ),
        migrations.AddField(
            model_name='carshowroomstock',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='carshowroom',
            name='date_of_creat',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 13, 37, 56, 616929)),
        ),
        migrations.AlterField(
            model_name='carshowroom',
            name='date_of_latest_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 13, 37, 56, 616929)),
        ),
    ]