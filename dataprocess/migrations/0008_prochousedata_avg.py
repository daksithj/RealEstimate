# Generated by Django 2.1.7 on 2019-03-29 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocess', '0007_prochousedata_raw'),
    ]

    operations = [
        migrations.AddField(
            model_name='prochousedata',
            name='avg',
            field=models.FloatField(default=0, null=True),
        ),
    ]