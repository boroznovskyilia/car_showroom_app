# Generated by Django 4.2.7 on 2023-11-17 10:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0011_alter_buyer_date_of_creat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='date_of_creat',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 13, 37, 56, 616929)),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='date_of_latest_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 13, 37, 56, 616929)),
        ),
        migrations.AlterField(
            model_name='transactionfromshowroomtobuyer',
            name='date_of_transaction',
            field=models.DateField(default='17/11/2023'),
        ),
    ]
