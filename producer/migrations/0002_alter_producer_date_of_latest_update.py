# Generated by Django 4.2.7 on 2023-11-13 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producer',
            name='date_of_latest_update',
            field=models.DateTimeField(),
        ),
    ]
