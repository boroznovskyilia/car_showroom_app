# Generated by Django 4.2.7 on 2023-11-13 12:14

import datetime
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0004_alter_buyer_balance_alter_buyer_date_of_creat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='date_of_creat',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 13, 15, 14, 30, 845616)),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='date_of_latest_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 13, 15, 14, 30, 845616)),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='location',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]