# Generated by Django 2.1.7 on 2019-04-05 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocess', '0010_auto_20190405_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housebacklog',
            name='land_availability',
        ),
        migrations.RemoveField(
            model_name='housebacklog',
            name='price',
        ),
        migrations.RemoveField(
            model_name='landbacklog',
            name='price',
        ),
        migrations.AlterField(
            model_name='backlogentries',
            name='date_searched',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 5, 16, 32, 50, 913111)),
        ),
    ]
