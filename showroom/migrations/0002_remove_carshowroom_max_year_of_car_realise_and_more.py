# Generated by Django 4.2.7 on 2023-11-13 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carshowroom',
            name='max_year_of_car_realise',
        ),
        migrations.RemoveField(
            model_name='carshowroom',
            name='min_year_of_car_realise',
        ),
    ]