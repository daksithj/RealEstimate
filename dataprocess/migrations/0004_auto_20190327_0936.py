# Generated by Django 2.1.7 on 2019-03-27 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocess', '0003_auto_20190326_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='proclanddata',
            name='hospital',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='proclanddata',
            name='temple',
            field=models.IntegerField(default=0),
        ),
    ]
